# coding: utf-8
"""
Django settings for helloworld project.

Generated by 'django-admin startproject' using Django 1.11.4.

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
SECRET_KEY = '5l-r-9^8g^ha11sjcpw^f+#s8bh2vakui2wmu**2l+3&9#80ec'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    #"django_forms_bootstrap",  ## forms_bootstrap
    "bootstrapform",
    'testModel',
    "book",
    "jobtask",
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.locale.LocaleMiddleware',  # 设置为本地的字符集
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'helloworld.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR,"templates"),],
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

WSGI_APPLICATION = 'helloworld.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     },
        'default':{
            "ENGINE":"django.db.backends.mysql",
            "HOST":"192.168.253.130",
            "NAME": "db_jobtask",
            "USER": "django",
            "PASSWORD": "dj123456",
            "PORT": 3306,
    },
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

# 英文
LANGUAGE_CODE = 'en-us'
# 中文，此版本此处配置无效
#LANGUAGE_CODE = "zh_CN"

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'

# set static files
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]


### add by qiueer
## add redis for cache
## 参考文档： http://django-redis-chs.readthedocs.io/zh_CN/latest/
## dependence:
## pip install django-redis
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://192.168.253.130:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "CONNECTION_POOL_KWARGS": {"max_connections": 100}, ## 连接池
            #"PASSWORD": "mysecret",   ## 密码
            "COMPRESSOR": "django_redis.compressors.zlib.ZlibCompressor",    ## 压缩
            #"COMPRESSOR": "django_redis.compressors.lzma.LzmaCompressor",  ## 压缩算法二，lzma
            "IGNORE_EXCEPTIONS": True,  ## 忽略异常
            "SOCKET_CONNECT_TIMEOUT": 5,  # in seconds，socket 建立连接超时设置
            "SOCKET_TIMEOUT": 5,  # in seconds， 连接建立后的读写操作超时设置
        }
    },
    "session": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://192.168.253.130:6379/2",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "COMPRESSOR": "django_redis.compressors.zlib.ZlibCompressor",    ## 压缩
            #"COMPRESSOR": "django_redis.compressors.lzma.LzmaCompressor",  ## 压缩算法二，lzma
            "IGNORE_EXCEPTIONS": True,  ## 忽略异常
        }
    }
}

### 将session写入到redis中 #####
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "session"

### RABBITMQ 配置信息
BROKER_HOST = "192.168.253.130"
BROKER_PORT = 5672
BROKER_USER = "guest"
BROKER_PASSWORD = "guest"
BROKER_VHOST = "/"