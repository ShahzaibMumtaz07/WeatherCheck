from .base import *
import sys

DEBUG = True
ALLOWED_HOSTS = ["127.0.0.1", "localhost"]
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "test_db",
        "USER": "postgres",
        "PASSWORD": "test@123",
        "HOST": "localhost",
        "PORT": "5432",
    },
}
if 'test' in sys.argv:
    DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "test_db",
        "USER": "postgres",
        "PASSWORD": "test@123",
        "HOST": "localhost",
        "PORT": "5432",
    },
}

TEST_RUNNER = 'weather_app.tests.utils.UnManagedModelTestRunner'


CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.db.DatabaseCache",
        "LOCATION": "my_cache",
        "KEY_PREFIX": "dev",
    }
}