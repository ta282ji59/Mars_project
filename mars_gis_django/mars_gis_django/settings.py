import os
import configparser
# from accounts import app
from pathlib import Path

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'l&*6jtn6(w0s04f=_!l!gnf4%syz%(fu3qhrt=sg)vu-rq763u'

# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = False
DEBUG = True

ALLOWED_HOSTS = ["*"]

# Application definition

INSTALLED_APPS = [
    'map3d',
    'spectra',
    'accounts',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.gis',

    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'rules.apps.AutodiscoverRulesConfig',
    'rest_framework',
    'widget_tweaks',
    'djgeojson',
    'corsheaders',
    'django_filters',
]

REST_FRAMEWORK = {
    'DEFAULT_FILTER_BACKENDS': ('django_filters.rest_framework.DjangoFilterBackend',)
}

SERIALIZATION_MODULES = {
    "geojson": "django.contrib.gis.serializers.geojson", 
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]

ROOT_URLCONF = 'mars_gis_django.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['map3d.templates','spectra.templates','accounts.templates'],
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

WSGI_APPLICATION = 'mars_gis_django.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'mars',
        'USER': 'm5211164',
        'PASSWORD': 'anpanman',
        'HOST': 'postgis',
        'PORT': '5432',
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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

AUTH_USER_MODEL = 'accounts.CustomUser'
SITE_ID = 1
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
    'accounts.auth_backends.DjangoBackend',
    # 'rules.permissions.ObjectPermissionBackend',
)
# # グループを作成する権限を付与
# GROUP_CREATION_PERMISSION = (
#     'groups.can_create_group',
# )

# Internationalization
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'
# TIME_ZONE = 'Asia/Tokyo'

USE_I18N = True

USE_L10N = True

# USE_TZ = True
USE_TZ = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

# テンプレート側でSTATICを呼び出す時のURL設定
STATIC_URL = '/collect_static/'

# プロジェクト全体に適用したいSTATICファイルがあれば活用する
# STATICFILES_DIRS = [
#     # os.path.join(BASE_DIR, 'static'), #プロジェクトディレクトリ直下のstaticファイル
#     os.path.join(BASE_DIR, 'collect_static'), #プロジェクトディレクトリ直下のstaticファイル
# ]

# 変更しない
# STATIC_ROOT: CSSファイルを1箇所に集める時、Webサーバ上でCSSを読み込みたい時に設定する
# collectstaticコマンド時にSTATIC_ROOTで指定したフォルダに全てのCSSファイルが集まる
STATIC_ROOT = os.path.join(BASE_DIR, 'collect_static/') #230617

LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/accounts/home'
# LOGIN_REDIRECT_URL = '/accounts/home_tmp'
LOGOUT_REDIRECT_URL = '/accounts/login'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# 認証方式はユーザー名
ACCOUNT_AUTHENTICATION_METHOD = 'username'
ACCOUNT_USERNAME_REQUIRED = True

# サインアップにメールアドレス確認を挟まない
ACCOUNT_EMAIL_VERIFICATION = 'none'
ACCOUNT_EMAIL_REQUIRED = False