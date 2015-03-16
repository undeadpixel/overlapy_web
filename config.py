import os

from recaptcha_config import *


# NOTICE: Remove this on production
DEBUG = True

# change base directory to get templates correctly
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

UPLOADS_PATH = os.path.join(BASE_DIR, "uploads")

# General flask stuff

SECRET_KEY = "blahblahblah"

# CSRF_SESSION_KEY = "blahblahblah"
# CSRF_ENABLED = True

# SQLAlchemy stuff

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'database.sqlite')

# Recaptcha stuff

RECAPTCHA_PARAMETERS = {'hl': 'zh', 'render': 'explicit'}
RECAPTCHA_DATA_ATTRS = {'theme': 'dark'}
