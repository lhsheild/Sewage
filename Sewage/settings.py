"""
Django settings for Sewage project.

Generated by 'django-admin startproject' using Django 1.11.20.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'q@l5%r4uqh@fxe$+k77^6zdwxer0qh$q5p6bpdl5m1inab$a)m'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['*',]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'ding_callback.apps.DingCallbackConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'Sewage.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'Sewage.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'sewage',  # 数据库名字(需要先创建)
        'USER': 'postgres',  # 登录用户名
        'PASSWORD': '123456',  # 密码
        'HOST': '',  # 数据库IP地址,留空默认为localhost
        'PORT': '5432',  # 端口
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

MEDIA_URL = '/media/'  #访问的前缀链接
MEDIA_ROOT = os.path.join(BASE_DIR, '../media')  #存放文件的具体位置

# 日志
ADMINS = (
    ('admin', '403613912@qq.com'),
)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.qq.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = '2693022425@qq.com'
EMAIL_HOST_PASSWORD = 'lh911016'
EMAIL_USE_SSL = True
EMAIL_SUBJECT_PREFIX = '[django] '
EMAIL_TIMEOUT = 3
DEFAULT_FROM_EMAIL = SERVER_EMAIL = EMAIL_HOST_USER

# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'filters': {
#         'request_id': {  # 自定义的filter
#             '()': 'log_request_id.filters.RequestIDFilter'
#         },
#         'require_debug_false': {
#             '()': 'django.utils.log.RequireDebugFalse',
#         }
#     },
#     'formatters': {
#         'standard': {
#             'format': '%(levelname)s [%(asctime)s] [%(request_id)s] %(filename)s-%(funcName)s-%(lineno)s: %(message)s'  # 这里使用filter request_id里的request_id字段
#         },
#         'default': {
#             'format': '%(levelname)s [%(asctime)s] %(name)s: %(message)s'
#         },
#     },
#     'handlers': {
#         'console': {
#             'level': 'DEBUG',
#             'class': 'logging.StreamHandler',
#             'filters': ['request_id'],  # 这里使用上面的filter: request_id
#             'formatter': 'standard',  # 这里使用上面的formatter: standard
#         },
#         'file': {  # 记录到日志文件(需要创建对应的目录，否则会出错)
#           'level': 'INFO',
#           'class': 'logging.handlers.RotatingFileHandler',
#           'filename': os.path.join(BASE_DIR, 'debug.log'),  # 日志输出文件
#           'maxBytes': 1024*1024*5,  # 文件大小
#           'backupCount': 5,  # 备份份数
#           'formatter': 'default',  # 使用哪种formatters日志格式
#          },
#         'mail_admins': {
#             'level': 'ERROR',
#             'class': 'django.utils.log.AdminEmailHandler',
#             'filters': ['require_debug_false'],
#             'include_html': True,
#         }
#     },
#     'loggers': {
#         'django': {
#             'handlers': ['file'],  # 这里使用上面的handler: console
#             'level': 'INFO',
#             'propagate': True,
#         },
#         'django.request': {
#             'handlers': ['file', 'mail_admins'],
#             'level': 'INFO',
#             'propagate': False
#         },
#         'project.app': {
#             'handlers': ['file', 'mail_admins'],
#             'level': 'INFO',
#             'propagate': True
#         }
#     }
# }