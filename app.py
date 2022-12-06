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
import urllib
import datetime as dt
from datetime import timezone
import humanize

# internal imports
import config
from db.db import query_db
from db.users import User
from db.links import add_new_link
from db.sql import (
    _QUERY_ALL_LINKS,
    _QUERY_SEARCH_LINKS,
    _GET_LINK,
    _GET_TAGNAMES,
    _QUERY_SEARCH_LINKS_BY_URL,
)

client = WebApplicationClient(config.GOOGLE_CLIENT_ID)

app = Flask(__name__)

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


def db_links_select(limit=5, offset=0):
    return query_db(_QUERY_ALL_LINKS, params=(limit, offset))


def db_links_search(title="%%", description="%%", limit=5, offset=0):
    return query_db(_QUERY_SEARCH_LINKS, params=(title, description, limit, offset))


def search_links_by_url(defragged="", limit=5, offset=0):
    return query_db(
        _QUERY_SEARCH_LINKS_BY_URL, params=(defragged, defragged, limit, offset)
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


@app.route("/add", methods=["GET", "POST"])
# @login_required
def add():
    if request.method == "GET":
        limit = request.args.get("limit", 5, type=int)
        page = request.args.get("page", 1, type=int)
        offset = (page - 1) * limit  # page=2, limit=10, offset = 10
        url = request.args.get("url", "", type=str)
        title = request.form.get("title", "", type=str)
        # if url is None and title is None:
        if url is None:
            links = []
        else:
            if url is not None:
                defragged = urllib.parse.urldefrag(url).url + "%"
            else:
                defragged = ""
            if title is None:
                title = "%%"
            links = search_links_by_url(
                defragged=defragged,
                # title=title,
                limit=limit,
                offset=offset,
            )
        return render_template(
            "add.html",
            current_user=current_user,
            links=links,
            page=page,
            limit=limit,
            offset=offset,
            title=title,
            defragged=defragged,
        )
    elif request.method == "POST":
        if current_user.is_authenticated:
            title = request.form.get("title")
            url = request.form.get("url")
            description = request.form.get("description")
            tags = request.form.get("tags", "")
            if tags == "":
                tag_names = []
            else:
                tag_names = tags.split(",")

            # return f'{request.form}'
            new_link = add_new_link(title, url, description, tag_names)
            return redirect("/add/" + str(new_link[0][0]))
    return render_template("add.html")


@app.route("/add/<int:link_id>")
def link_get(link_id):
    inserted = query_db(
        _GET_LINK,
        params=(link_id,),
    )
    tags_for_inserted = query_db(
        _GET_TAGNAMES,
        params=(link_id,),
    )
    link = inserted[0]
    tags = ""
    if len(tags_for_inserted) > 0:
        tags = "".join(tags_for_inserted[0])
    created_at = humanize.naturaltime(dt.datetime.now(timezone.utc) - link.datecreated)
    return render_template(
        "link.html",
        link_id=link_id,
        title=link.title,
        url=link.url,
        description=link.description,
        created_at=created_at,
        tags=tags,
    )
    # return f'<li>{link_id} - {created_at} - <a href="{link.url}">{link.title}</a> {link.description} ({tags})</li>'  # noqa
    # return f"""
    #     <li>{link_id} - {created_at} - <a href="{link.url}">
    #     {link.title}</a> {link.description} ({tags})</li>
    # """


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

    return render_template(
        "search.html",
        links=links,
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

    return render_template(
        "search.html",
        links=links,
        page=page,
        limit=limit,
        offset=offset,
        searchterm=searchterm,
        current_user=current_user,
    )
