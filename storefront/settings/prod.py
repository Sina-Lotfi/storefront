import os
from pickle import FALSE
import dj_database_url
from storefront.settings.dev import SECRET_KEY
from .common import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = FALSE
SECRET_KEY = os.environ["SECRET_KEY"]
ALLOWED_HOSTS = []
DATABASES = {"default": dj_database_url.config()}
REDIS_URL = os.environ["REDIS_URL"]
CELERY_BROKER_URL = REDIS_URL
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": REDIS_URL,
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    }
}
EMAIL_HOST = os.environ["MAILGUN_SMTP_SERVER"]
EMAIL_HOST_USER = os.environ["MAILGUN_SMTP_LOGIN"]
EMAIL_HOST_PASSWORD = os.environ["MAILGUN_SMTP_PASSWORD"]
EMAIL_PORT = os.environ["MAILGUN_SMTP_PORT"]
