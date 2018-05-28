import os
import socket

from celery.schedules import crontab
from django.utils.translation import gettext_lazy as _
from django.contrib import admin


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

admin.site.site_title = _('Django site admin')
admin.site.site_header = _('Django administration')
admin.site.index_title = _('Site administration')
admin.site.site_url = '/admin/'


class Env:
    """Env"""

    SECRET_KEY = ')&!pn-u*ijid#&*nzcvse!w^b1#o3ix)cilvq+838yov$q5o1i'

    DEBUG = True

    ALLOWED_HOSTS = ['*']

    ROOT_URLCONF = 'djrest.urls'

    WSGI_APPLICATION = 'djrest.wsgi.application'

    LANGUAGE_CODE = 'en-us'
    TIME_ZONE = 'UTC'
    USE_I18N = True
    USE_L10N = True
    USE_TZ = True

    LOCALE_PATHS = (
        os.path.join(BASE_DIR, 'locale'),
    )

    STATIC_URL = '/static/'
    STATIC_ROOT = 'collectstatic'

    STATICFILES_DIRS = (
        os.path.join(BASE_DIR, 'static'),
    )

    MEDIA_URL = '/media/'
    MEDIA_ROOT = 'media'

    EMAIL_HOST = 'smtp.gmail.com'
    EMAIL_PORT = 587
    EMAIL_USE_TLS = True
    EMAIL_HOST_USER = 'djrest1992@gmail.com'
    EMAIL_HOST_PASSWORD = '|-|(0)m3'

    DEFAULT_FROM_EMAIL = 'djrest1992@gmail.com'

    CORS_ORIGIN_ALLOW_ALL = True
    CORS_ORIGIN_WHITELIST = ()
    CORS_ALLOW_METHODS = (
        'GET', 'POST', 'PUT',
        'PATCH', 'DELETE', 'OPTIONS',
    )
    CORS_ALLOW_HEADERS = (
        'accept', 'accept-encoding', 'authorization',
        'content-type', 'dnt', 'origin', 'user-agent',
        'x-csrftoken', 'x-requested-with', 'time-zone',
    )

    # Django channels framework: Project that takes Django and extends its abilities beyond HTTP - to handle WebSockets, chat protocols, IoT protocols, and more.

    ASGI_APPLICATION = 'djrest.routing.application'

    CHANNEL_LAYERS = {
        'default': {
            'BACKEND': 'channels_redis.core.RedisChannelLayer',
            'CONFIG': {
                'hosts': [('localhost', 6379)],
           },
        },
    }

    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        },
    }

    # CACHES = {
    #     'default': {
    #         'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
    #         'LOCATION': '127.0.0.1:11211',
    #     },
    # }

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        },
    }

    # DATABASES = {
    #     'default': {
    #         'ENGINE': 'django.db.backends.postgresql',
    #         'NAME': 'djdb',
    #         'USER': 'djuser',
    #         'PASSWORD': 'p455w0rd',
    #         'HOST': 'localhost',
    #         'PORT': '5432',
    #     },
    # }

    # DATABASES = {
    #     'default': {
    #         'ENGINE': 'django.db.backends.mysql',
    #         'NAME': 'djdb',
    #         'USER': 'djuser',
    #         'PASSWORD': 'p455w0rd',
    #         'HOST': 'localhost',
    #         'PORT': '3306',
    #         'OPTIONS': {
    #             'init_command': 'SET sql_mode=\'STRICT_TRANS_TABLES\'',
    #         }
    #     }
    # }

    AUTH_TOKEN_EXPIRE = 316224000 # 10 years

    SIGNUP_CODE_EXPIRE = 600 # 10 minutes
    SIGNUP_EMAIL_USE_LIMIT = 5 # 5 times

    PASSWD_RESET_TOKEN_EXPIRE = 600 # 10 minutes
    PASSWD_RESET_URL = 'http://localhost:8000/accounts/me/passwd/reset'

    # Firebase Cloud Messaging

    FCM_TOKEN = 'AAAAcA3b7Is:APA91bFOjWJKMDljaXTgiSw_CYHdpo7yY-GRTzq0kG8eo_f75LCLtM1YC0EH-ZW_VzoQnxbYQxSraMiQ-8oUhMC__gM46igqOrN9hEgZlQZeWovWg4hiobIa_1j9PNq8v3fGOAVGpxbu'
    FCM_SENDER_ID = '481268853899'
    FCM_URL = 'https://fcm.googleapis.com/fcm/send'
    FCM_DEFAULT_ICON = '/images/fcm.png'

    # Login with Facebook

    FACEBOOK_API = 'https://graph.facebook.com/v2.12'

    # Celery: Distributed task queue. Celery is an asynchronous task queue/job queue based on distributed message passing.

    CELERY_BROKER_URL = 'sqla+sqlite:///celery.sqlite3'
    CELERY_RESULT_BACKEND = 'db+sqlite:///celery.sqlite3'

    # CELERY_BROKER_URL = 'redis://localhost:6379/0'
    # CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'

    CELERY_BEAT_SCHEDULE = {
        'run-every-minute': {
            'task': 'common.tasks.add',
            'schedule': crontab(),
            'args': (2, 5),
        },
    }

    CELERY_BEAT_SCHEDULER = 'celery.beat:PersistentScheduler'
    CELERY_BEAT_SCHEDULE_FILENAME = 'schedule.db'

    # Sentry: Error tracking that helps developers monitor and fix crashes in real time.

    USE_SENTRY = False
    RAVEN_CONFIG = {
        'dsn': 'https://afb2183da948402b905928b5b522d62a:851e958dc5124530a2c41631a55c4c94@sentry.io/270851',
    }


class ExampleEnv(Env):
    """Example env"""

    DEBUG = True


class DevelopmentEnv(Env):
    """Development env"""

    DEBUG = True

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'd7dqns5m0fs872',
            'USER': 'sxtmxkernwdmdr',
            'PASSWORD': '7d9ec1636115946d95ecc091e0917106232f8b1607d46cb9208f6b8fce7c0f62',
            'HOST': 'ec2-23-23-142-5.compute-1.amazonaws.com',
            'PORT': '5432',
        },
    }

    USE_SENTRY = True


class TestingEnv(Env):
    """Testing env"""

    DEBUG = True

    USE_SENTRY = True


class ProductionEnv(Env):
    """Production env"""

    DEBUG = False

    USE_SENTRY = True


envs = {
    'example': ExampleEnv,
    'development': DevelopmentEnv,
    'testing': TestingEnv,
    'production': ProductionEnv,
}

env = envs.get(os.environ.get(
    'ENV_NAME') or socket.gethostname(), Env)()
