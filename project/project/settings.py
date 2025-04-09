
from pathlib import Path
import os
from dotenv import load_dotenv
load_dotenv()  # Load .env file

#KHALTI_URL = os.getenv("KHALTI_URL")
# Debugging: Print to check if KHALTI_URL is loaded
#print(f"KHALTI_URL from env: {KHALTI_URL}")
KHALTI_AUTH = os.getenv("KHALTI_AUTH", "").strip()  # Remove any extra spaces
KHALTI_URL = os.getenv("KHALTI_URL")

# Ensure the "Key " prefix is added in the header
KHALTI_AUTH_HEADER = f"Key {KHALTI_AUTH}"



LOGIN_URL = "/login/"  # URL for the login page
LOGIN_REDIRECT_URL = "/home/"  # URL to redirect to after login  # Replace with correct API URL



# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-v)ieewt7iycoewccvau+%le*-)9=7vg-$)$xo=_kje#i$y*9&8'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['.render.com']




# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'app1',
    'cart',
    'payment',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates', ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'cart.context_processors.cart',
            ],
        },
    },
]

WSGI_APPLICATION = 'project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

STATICFILES_DIRS =['static/']
MEDIA_URL = 'media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# payment gateway configurations
TRANSACTION_REDIRECT_URL = os.getenv("TRANSACTION_REDIRECT_URL")
WEBSITE_URL = os.getenv("WEBSITE_URL")

# khalti configurations
KHALTI_CUSTOMER_NAME = os.getenv("KHALTI_CUSTOMER_NAME")
KHALTI_CUSTOMER_EMAIL = os.getenv("KHALTI_CUSTOMER_EMAIL")
KHALTI_CUSTOMER_PHONE = os.getenv("KHALTI_CUSTOMER_PHONE")
KHALTI_MERCHANT_USERNAME = os.getenv("KHALTI_MERCHANT_USERNAME")
KHALTI_AUTH = os.getenv("KHALTI_AUTH")
KHALTI_URL = os.getenv("KHALTI_URL")
KHALTI_LOOKUP_URL = os.getenv("KHALTI_LOOKUP_URL")

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
