import json
import requests

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
import datetime as dt
from datetime import timezone
import humanize


# internal imports
import config
from db import query_db
from db.users import User
from db.links import (
    add_new_link,
    tag_string_to_list,
    db_get_tag_names_mapped_to_link,
)
from db.sql import (
    QUERY_ALL_LINKS,
    QUERY_ALL_TAGS,
    QUERY_TAGS_COUNT,
    QUERY_SEARCH_LINKS,
    QUERY_SEARCH_COUNT,
    GET_LINK,
    GET_TAGNAMES,
    QUERY_GET_TAG_LINKS,
    QUERY_GET_TAG_LINKS_COUNT,
    SEARCH_FOR_POTENTIAL_DUPES,
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
    return requests.get(config.GOOGLE_DISCOVERY_URL).json()


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


# def pagination_params():
# todo move limit, page, offset into a function


@app.route("/")
def index():
    limit = request.args.get("limit", 10, type=int)
    page = request.args.get("page", 1, type=int)
    offset = (page - 1) * limit  # page=2, limit=10, offset = 10

    # make a link object and add this as a method
    # timesince = humanize.naturaldelta(dt.timedelta(datecreated))

    links = db_links_select(
        limit=limit,
        offset=offset,
    )

    return render_template(
        "index.html",
        links=links,
        context_name_for_sheri="stuff",
        limit=limit,
        page=page,
        offset=offset,
        current_user=current_user,
    )


@app.route("/login")
def login():
    if config.AUTOLOGIN:
        user = User.get_from_email(config.DEV_EMAIL)
        login_user(user)
        return redirect(url_for("index"))

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
    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code,
    )
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(config.GOOGLE_CLIENT_ID, config.GOOGLE_CLIENT_SECRET),
    )

    # parse the tokens
    client.parse_request_body_response(json.dumps(token_response.json()))

    # get profile information from google
    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)

    # make sure email is verified with google
    if userinfo_response.json().get("email_verified"):
        users_email = userinfo_response.json()["email"]
        picture = userinfo_response.json()["picture"]
        users_name = userinfo_response.json()["given_name"]

        # if the user doesn't exist locally, deny access
        user = User.get_from_email(users_email)
        # if not User.get(unique_id):
        #     User.create(unique_id, users_name, users_email, picture)
        if user is None:
            # raise ValueError(f"NO USER! {users_email}")
            user = User.create(users_name, users_email, picture)
        # Begin user session by logging the user in
        # user = User(
        #     id_=unique_id, name=users_name, email=users_email, profile_pic=picture
        # )
        login_user(user)
        # Send user back to homepage
        return redirect(url_for("index"))
    else:
        return "User email not available or not verified by Google.", 400


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))


@app.route("/profile")
def profile():
    if current_user.is_authenticated:
        return jsonify(
            name=current_user.name,
            email=current_user.email,
            pic=current_user.profile_pic,
        )
    else:
        return redirect(url_for("login"))
        # return jsonify(error='unauthorized' ), 403


def tag_string_to_list(tags):
    if tags == "":
        return []
    else:
        tag_names = tags.split(",")
        tag_list = [tag.strip() for tag in tag_names]
        return tag_list


def tag_list_to_string(tags):
    if len(tags) == 0:
        return ""
    else:
        tag_names = ", ".join(tags)
        return tag_names


@app.route("/add", methods=["GET", "POST"])
# @login_required
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
            return render_template(
                "add.html",
                links=links,
                page=page,
                limit=limit,
                offset=offset,
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


@dataclass
@app.route("/link/<int:link_id>")
def link(link_id):
    link = query_db(GET_LINK, params=(link_id,))
    link = link[0]
    tag_names = db_get_tag_names_mapped_to_link(link_id)
    tag_names_joined = ", ".join(tag_names)
    created_at = humanize.naturaltime(dt.datetime.now(timezone.utc) - link.datecreated)
    return render_template(
        "link.html",
        link=link,
        link_id=link.id,
        title=link.title,
        url=link.url,
        description=link.description,
        tags=tag_names_joined,
        created_at=created_at,
    )
    # debugging example
    # return f"""
    #     <li>{link_id} - {created_at} - <a href="{link.url}">
    #     {link.title}</a> {link.description} ({tags})</li>
    # """ # noqa


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
