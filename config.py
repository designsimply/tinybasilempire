import os


def as_bool(str_value):
    return bool(str_value == "true")


GOOGLE_CLIENT_ID = os.environ["GOOGLE_CLIENT_ID"]
GOOGLE_CLIENT_SECRET = os.environ["GOOGLE_CLIENT_SECRET"]
GOOGLE_DISCOVERY_URL = "https://accounts.google.com/.well-known/openid-configuration"
SECRET_KEY = os.environ.get("SECRET_KEY")

DB_HOST = os.environ.get("POSTGRES_HOST")
DB_NAME = os.environ.get("POSTGRES_DB_NAME")
DB_USER = os.environ.get("POSTGRES_USER")
DB_PASS = os.environ.get("POSTGRES_PASSWORD")

AUTOLOGIN = as_bool(os.environ["AUTOLOGIN"])
DEV_EMAIL = os.environ["DEV_EMAIL"]
NGINX_SERVER_NAME = os.environ.get("NGINX_SERVER_NAME")
SEARCHFORM_PLACEHOLDER = os.environ["SEARCHFORM_PLACEHOLDER"]
