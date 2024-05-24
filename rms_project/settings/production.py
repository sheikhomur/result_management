from .base import *
import os


WEBSITE_BASE_URL = "https://localhost:3000"
WEBSITE_BACKEND_URL = "https://localhost:8000"

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

ALLOWED_HOSTS = ['*']

DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': os.environ.get('DB_HOST'),
        'PORT': os.environ.get('DB_PORT'),
    }
}

WKHTMLTOPDF_PATH = "/usr/bin/wkhtmltopdf"
