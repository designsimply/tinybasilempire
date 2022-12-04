import os

GOOGLE_CLIENT_ID = os.environ['GOOGLE_CLIENT_ID']
GOOGLE_CLIENT_SECRET = os.environ['GOOGLE_CLIENT_SECRET']
GOOGLE_DISCOVERY_URL = 'https://accounts.google.com/.well-known/openid-configuration'

AUTOLOGIN = bool(os.environ['AUTOLOGIN'])
DEV_EMAIL = os.environ['DEV_EMAIL']
