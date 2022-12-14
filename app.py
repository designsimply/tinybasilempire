import json
import urllib3

# third-party libraries
from flask import Flask, render_template, redirect, request, url_for, jsonify
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)
from oauthlib.oauth2 import WebApplicationClient
from dataclasses import dataclass
import urllib


# internal imports
import config
from db import query_db
from db.users import User
from db.links import (
    add_new_link,
    tag_string_to_list,
    db_get_tag_names_mapped_to_link,
    update_link,
    format_link_dates,
    delete_link_and_mapped_tags,
)
from db.sql import (
    QUERY_ALL_LINKS,
    QEURY_LINKS_COUNT,
    QUERY_ALL_TAGS,
    QUERY_TAGS_COUNT,
    QUERY_SEARCH_LINKS,
    QUERY_SEARCH_COUNT,
    GET_LINK,
    QUERY_GET_TAG_LINKS,
    QUERY_GET_TAG_LINKS_COUNT,
    SEARCH_FOR_POTENTIAL_DUPES,
    SEARCH_FOR_POTENTIAL_DUPES_COUNT,
)
from flask_sslify import SSLify

client = WebApplicationClient(config.GOOGLE_CLIENT_ID)

app = Flask(__name__)
sslify = SSLify(app)
app.secret_key = config.SECRET_KEY

# user session management setup from
# https://flask-login.readthedocs.io/en/latest
login_manager = LoginManager()
login_manager.init_app(app)


# find out what url to hit for google login
def get_google_provider_cfg():
    with urllib3.PoolManager() as http:
        response = http.request("GET", config.GOOGLE_DISCOVERY_URL)
        data = json.loads(response.data.decode("utf8"))
    return data


# flask-login helper to retrieve a user from the db
@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


# friendlier formats for time since
def strfdelta(tdelta, fmt):
    d = {"days": tdelta.days}
    d["hours"], rem = divmod(tdelta.seconds, 3600)
    d["minutes"], d["seconds"] = divmod(rem, 60)
    return fmt.format(**d)


# make strfdelta function available in all templates
app.jinja_env.globals["strfdelta"] = strfdelta


def db_links_select(limit=5, offset=0):
    return query_db(QUERY_ALL_LINKS, params=(limit, offset))


def db_links_count():
    return query_db(QEURY_LINKS_COUNT)


def db_tags_select(limit=5, offset=0):
    return query_db(QUERY_ALL_TAGS, params=(limit, offset))


def db_tags_count():
    return query_db(QUERY_TAGS_COUNT)


def db_tag_links(tag_name="%%", limit=10, offset=0):
    return query_db(QUERY_GET_TAG_LINKS, params=(tag_name, limit, offset))


def db_tag_links_count(tag_name="%%"):
    return query_db(QUERY_GET_TAG_LINKS_COUNT, params=[tag_name])


def db_links_search(title="%%", description="%%", limit=5, offset=0):
    return query_db(QUERY_SEARCH_LINKS, params=(title, description, limit, offset))


def db_links_search_count(title="%%", description="%%"):
    return query_db(QUERY_SEARCH_COUNT, params=(title, description))


def search_links_by_defragged_url(fuzzy, defragged, limit=5, offset=0):
    return query_db(
        SEARCH_FOR_POTENTIAL_DUPES, params=(fuzzy, defragged, limit, offset)
    )


def search_links_by_defragged_url_count(fuzzy, defragged):
    return query_db(SEARCH_FOR_POTENTIAL_DUPES_COUNT, params=[fuzzy, defragged])


# def pagination_params():
# todo move limit, page, offset into a function


@app.route("/")
def index():
    return render_template(
        "base.html",
        current_user=current_user,
    )


@app.route("/latest")
def latest():
    limit = request.args.get("limit", 10, type=int)
    page = request.args.get("page", 1, type=int)
    offset = (page - 1) * limit
    total = db_links_count()

    links = db_links_select(
        limit=limit,
        offset=offset,
    )

    return render_template(
        "latest.html",
        links=links,
        limit=limit,
        page=page,
        offset=offset,
        total=total[0].count,
        current_user=current_user,
    )


@app.route("/login")
def login():
    if config.AUTOLOGIN:
        user = User.get_from_email(config.DEV_EMAIL)
        login_user(user)
        return redirect(url_for("latest"))

    # get a login url for google
    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]

    # request google login and scope what to retrieve
    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=request.base_url + "/callback",
        scope=["openid", "email", "profile"],
    )
    return redirect(request_uri)


@app.route("/login/callback")
def callback():
    # get auth code back from google
    code = request.args.get("code")

    # get google authorization code and url for tokens
    google_provider_cfg = get_google_provider_cfg()
    token_endpoint = google_provider_cfg["token_endpoint"]

    # send a request to get tokens
    token_url, token_headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code,
    )
    with urllib3.PoolManager() as http:
        auth_headers = urllib3.make_headers(
            basic_auth=f"{config.GOOGLE_CLIENT_ID}:{config.GOOGLE_CLIENT_SECRET}"
        )

        headers = {**token_headers, **auth_headers}
        response = http.request(
            "POST",
            token_url,
            headers=headers,
            body=body,
        )
        token_response = json.loads(response.data.decode("utf8"))

    # parse the tokens
    client.parse_request_body_response(json.dumps(token_response))

    # get profile information from google
    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    with urllib3.PoolManager() as http:
        response = http.request("GET", uri, headers=headers, body=body)
        userinfo = json.loads(response.data.decode("utf8"))

    # make sure email is verified with google
    if userinfo.get("email_verified"):
        users_email = userinfo["email"]
        picture = userinfo["picture"]
        users_name = userinfo["given_name"]

        # if the user doesn't exist locally, deny access
        # else use Google data to update our database
        user = User.get_from_email(users_email)
        if user is None:
            error = f"{users_email}, I don't know you! Only known users are allowed."
            return render_template(
                "404.html",
                error=error,
            )
        else:
            user = User.update(users_name, users_email, picture)
            # Begin user session by logging the user in
            # user = User(
            #     id_=unique_id, name=users_name, email=users_email, profile_pic=picture
            # )
            login_user(user)
        # Send user back to latest endpoint
        return redirect(url_for("latest"))
    else:
        return "User email not available or not verified by Google.", 400


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("latest"))


@app.route("/profile")
@login_required
def profile():
    if current_user.is_authenticated:
        return jsonify(
            email=current_user.email,
            name=current_user.name,
            pic=current_user.profile_pic,
        )
    else:
        return redirect(url_for("login"))
        # return jsonify(error='unauthorized' ), 403


@app.route("/add", methods=["GET", "POST"])
@login_required
def add():
    if request.method == "GET":
        limit = request.args.get("limit", 5, type=int)
        page = request.args.get("page", 1, type=int)
        offset = (page - 1) * limit  # page=2, limit=10, offset = 10
        url = request.args.get("url", "", type=str)
        title = request.form.get("title", "", type=str)

        if len(url) > 0:
            defragged = urllib.parse.urldefrag(url).url
            links = search_links_by_defragged_url(
                fuzzy=defragged + "%",
                defragged=defragged,
                limit=limit,
                offset=offset,
            )

            count = search_links_by_defragged_url_count(
                fuzzy=defragged + "%", defragged=defragged
            )
            total = count[0].count

            return render_template(
                "add.html",
                links=links,
                page=page,
                limit=limit,
                offset=offset,
                total=total,
                defragged=defragged,
            )
        else:
            return render_template("add.html")

    elif request.method == "POST":
        if current_user.is_authenticated:
            title = request.form.get("title")
            url = request.form.get("url")
            description = request.form.get("description")
            tags = request.form.get("tags", "")
            tag_list = tag_string_to_list(tags)
            link, tag_list = add_new_link(title, url, description, tag_list)
            return redirect("/link/" + str(link.id))
    return render_template("add.html")


@dataclass
class EditForm:
    """This is for the Edit Link Form values."""

    title: str
    url: str
    description: str
    tags: str


@app.route("/edit/<int:link_id>", methods=["GET", "POST"])
@login_required
def edit(link_id):
    links = []
    links = query_db(GET_LINK, params=(link_id,))

    if len(links) < 1:
        link = []
        error = f"A search for link id {link_id} returned zero results."
        return render_template(
            "404.html",
            error=error,
        )

    else:
        link = links[0]
        link_meta = format_link_dates(link)
        tag_names_from_db = db_get_tag_names_mapped_to_link(link_id)
        tag_names_from_db_joined = ", ".join(tag_names_from_db)

        if request.method == "POST":
            form = EditForm(**request.form)
            link, tags_mapped, tags_unmapped = update_link(
                link_id, form.title, form.url, form.description, form.tags
            )
            if link:
                return redirect("/link/" + str(link.id))

        return render_template(
            "edit.html",
            links=links,
            link_id_string=str(link_id),
            tags=tag_names_from_db_joined,
            link_meta=link_meta,
        )


@app.route("/link/<int:link_id>")
def link(link_id):
    links = query_db(GET_LINK, params=(link_id,))
    if len(links) > 0:
        link = links[0]
        link_meta = format_link_dates(link)
        tag_names = db_get_tag_names_mapped_to_link(link_id)

        return render_template(
            "link.html",
            links=links,
            tags=tag_names,
            link_meta=link_meta,
        )
    else:
        link = []
        error = f"Record {link_id} was not found."
        return render_template(
            "404.html",
            error=error,
        )


@app.route("/delete/<int:link_id>", methods=["GET", "POST"])
@login_required
def delete(link_id):
    links = query_db(GET_LINK, params=(link_id,))
    if len(links) > 0:
        link = links[0]
        tag_names = db_get_tag_names_mapped_to_link(link_id)
        link_meta = format_link_dates(link)

        if request.method == "POST":
            if request.form.get("ays") == "Yes":
                deleted = delete_link_and_mapped_tags(link_id)
                return render_template(
                    "delete.html",
                    deleted_link_id=deleted[0].link_id,
                )

        return render_template(
            "delete.html",
            links=links,
            tags=tag_names,
            link_meta=link_meta,
        )
    else:
        link = []
        error = f"Record {link_id} was not found."
        return render_template(
            "404.html",
            error=error,
        )


@app.route("/tags")
def tags():
    limit = request.args.get("limit", 60, type=int)
    page = request.args.get("page", 1, type=int)
    offset = (page - 1) * limit  # page=2, limit=10, offset = 10

    tags = db_tags_select(
        limit=limit,
        offset=offset,
    )

    total = db_tags_count()

    return render_template(
        "tags.html",
        tags=tags,
        limit=limit,
        offset=offset,
        page=page,
        total=total[0].count,
        current_user=current_user,
    )


@app.route("/tag/<string:tag_name>")
def tag(tag_name):
    limit = request.args.get("limit", 10, type=int)
    page = request.args.get("page", 1, type=int)
    offset = (page - 1) * limit

    links = db_tag_links(
        tag_name=tag_name,
        limit=limit,
        offset=offset,
    )

    count = db_tag_links_count(tag_name=tag_name)
    total = count[0].count

    return render_template(
        "search.html",
        links=links,
        total=int(total),
        page=page,
        limit=limit,
        offset=offset,
        tag_name=tag_name,
        current_user=current_user,
    )


@app.route("/search")
def s():
    searchterm = ""
    if request.args.get("q"):
        searchterm = request.args.get("q")

    limit = request.args.get("limit", 5, type=int)
    page = request.args.get("page", 1, type=int)
    offset = (page - 1) * limit  # page=2, limit=10, offset = 10

    links = db_links_search(
        title=searchterm,
        description=searchterm,
        limit=limit,
        offset=offset,
    )

    count = db_links_search_count(title=searchterm, description=searchterm)
    total = count[0].count

    return render_template(
        "search.html",
        links=links,
        total=total,
        page=page,
        limit=limit,
        offset=offset,
        searchterm=searchterm,
        current_user=current_user,
    )


@app.route("/s/<string:searchterm>")
def search(searchterm):
    limit = request.args.get("limit", 5, type=int)
    page = request.args.get("page", 1, type=int)
    offset = (page - 1) * limit  # page=2, limit=10, offset = 10

    links = db_links_search(
        title=searchterm,
        description=searchterm,
        limit=limit,
        offset=offset,
    )

    count = db_links_search_count(title=searchterm, description=searchterm)
    total = count[0].count

    return render_template(
        "search.html",
        links=links,
        total=int(total),
        page=page,
        limit=limit,
        offset=offset,
        searchterm=searchterm,
        current_user=current_user,
    )
