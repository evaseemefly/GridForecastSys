"""
Django settings for GridForecastSys project.

Generated by 'django-admin startproject' using Django 2.0.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os
import sys

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# 将当前路径加入到系统索引中
sys.path.insert(0, BASE_DIR)
# 将所有的app统一放在apps文件夹中
sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'n7cni@q7m4zbmtsd4z0%t31#czti=_2^^qelkq76p+(5uo3hu1'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# 加入跨域访问允许的端口
ALLOWED_HOSTS = [
    'localhost:8015',
    '127.0.0.1:8015',
    '127.0.0.1:8000',
    '127.0.0.1'
]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 跨域的app
    'corsheaders',
    'GridForecast',
    'Station',
    'StormTide',
    'Fub',
    # django rest framework
    'rest_framework',
    # 'xadmin',
    # 'crispy_forms',
    # 'reversion',

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    # 添加cors
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# 跨域增加忽略
CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_ALLOW_ALL = True
# 白名单
# CORS_ORIGIN_WHITELIST = (
#     # '*'
#     'localhost:8015',
#     '127.0.0.'
# )

# CORS_ALLOW_METHODS = (
#     'DELETE',
#     'GET',
#     'OPTIONS',
#     'PATCH',
#     'POST',
#     'PUT',
#     'VIEW',
# )

# CORS_ALLOW_HEADERS = (
#
#     'accept',
#     'accept-encoding',
#     'authorization',
#     'XMLHttpRequest',
#     'X_FILENAME',
#     'accept-encoding',
#     'authorization',
#     'content-type',
#     'dnt',
#     'origin',
#     'user-agent',
#     'x-csrftoken',
#     'x-requested-with',
#     'Pragma',
# )

ROOT_URLCONF = 'GridForecastSys.urls'

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

WSGI_APPLICATION = 'GridForecastSys.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        # 'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        'NAME': 'gridforecast',
        # w540
        'USER': 'root',
        'PASSWORD': '123456',
        # 单位台式机
        # 'USER':'admin',
        # 'PASSWORD':'admin123',
        # 'HOST':'127.0.0.1',
        # p52s
        # 'USER':'root',
        # 'PASSWORD':'123456',
        # 'HOST':'127.0.0.1',

        # mac
        # 'USER':'root',
        # 'PASSWORD':'12345678'
        # mac 840
        # 'USER':'root',
        # 'PASSWORD':'nmefc123'

        # 'HOST':'127.0.0.1',
        # 'OPTIONS':{'init_command':'SET storage_engine=INNODB;'}
    }
}

# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

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

REST_FRAMEWORK = {
    'DATETIME_FORMAT': "%m-%d %H",
}
# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

# 时区改为上海时
TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
    ('mapfiles', os.path.join(STATIC_URL, 'mapfiles').replace('\\', '/')),
    '/Users/liusihan'
]

AreaNames_DIR = r'D:\git仓库\GridForecastSys\extra_data\grid_data'
AreaNames_FilesName = ['names_S', 'names_N', 'names_E']
AreaNames_Dict = {'n': 'names_N', 'e': 'names_E', 's': 'names_S'}

NCReader_DIR = r'/Users/liusihan/Documents/01project/GridForecastSys/extra_data/nc_data'

# celery需要的相关配置
CELERY_BROKER_URL = 'redis://127.0.0.1:6379/0'
CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/0'
CELERY_TASK_ERIALIZER = 'json'
