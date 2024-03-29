import os
from pathlib import Path

from decouple import config
from django.urls import reverse_lazy

BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=True, cast=bool)

ALLOWED_HOSTS = ['127.0.0.1','localhost']  # takeaway.com for production

# Application definition

INSTALLED_APPS = [
    'admin_interface',
    'colorfield',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'accounts.apps.AccountsConfig',
    'orders.apps.OrdersConfig',
    'storages',  # django-storages - S3
    'phonenumber_field',  # django-phonenumber-field
    'markdown_view',
    'fontawesomefree',
]

MIDDLEWARE = [

    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',  # works with django.contrib.auth
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    #  'takeaway.middlewares.handle_exception',
]

ROOT_URLCONF = 'takeaway.urls'

# sessions that are created are expired on browser close by default
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'takeaway.context_processors.common_variables',
            ],
        },
    },
]

WSGI_APPLICATION = 'takeaway.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('HOST'),
        'PORT': config('DB_PORT'),
    }
}

# Redis Cache - to start: redis-server
CACHES = {
  'default': {
    'BACKEND': 'django.core.cache.backends.redis.RedisCache',
    'LOCATION': 'redis://127.0.0.1:6379',
  }
}

# CELERY STUFF
CELERY_BROKER_URL = 'redis://localhost:6379//'
CELERY_RESULT_BACKEND = 'redis://localhost:6379'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
#  to start celery:
#!!!!  celery -A takeaway worker --loglevel=INFO --concurrency 1 -P solo

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


STATIC_URL = 'static/'
STATICFILES_DIRS = [
    BASE_DIR / 'static/',
]


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


AUTH_USER_MODEL = 'accounts.CustomUser'

LOGIN_URL = reverse_lazy('login')  # to look for accounts/login, not auth/login
LOGOUT_REDIRECT_URL = 'home'  # django admin logout

USE_S3 = True

if USE_S3:
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

    # aws settings
    AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY')
    AWS_SECRET_ACCESS_KEY = config('AWS_SECRET')
    AWS_STORAGE_BUCKET_NAME = config('AWS_BUCKET')
    AWS_S3_REGION_NAME = config('AWS_REGION')

#  files with the same name will overwrite each other.
    AWS_S3_FILE_OVERWRITE = True
    AWS_DEFAULT_ACL = None

    AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
    AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'max-age=86400'}

    # s3 public media settings
    PUBLIC_MEDIA_LOCATION = 'media'
    MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{PUBLIC_MEDIA_LOCATION}/'

else:

    # Base url to serve media files
    MEDIA_URL = 'media/'

    # Path where media is stored
    MEDIA_ROOT = BASE_DIR / 'media/'

# SMTP Configurations
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = 'True'
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')

PHONENUMBER_DB_FORMAT = "NATIONAL"
PHONENUMBER_DEFAULT_REGION = "BG"

# for django admin themes
X_FRAME_OPTIONS = 'SAMEORIGIN'

# Logging
# https://docs.djangoproject.com/en/4.0/topics/logging/
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,

    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },

    'handlers': {
        'console': {
            'level': 'DEBUG',
            'filters': [],
            'class': 'logging.StreamHandler',
        },
        'file': {
            # all levels - DEBUG,INFO,WARNING,ERROR,CRITICAL
            'class': 'logging.FileHandler',
            'filename': 'general.log',
            'formatter': 'simple',
        },
    },

    'root': {
        'handlers': ['file'],
        'level': 'INFO',  # up from level INFO
    },

    'loggers': {
        'django.db.backends': {
            'handlers': ['file'],
        },
    },
}
