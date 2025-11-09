import os
from pathlib import Path
from dotenv import load_dotenv
from cryptography.fernet import Fernet


BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = "django-insecure-+k3v#(u8qz$y7v1&l5@8m3v1xj$z9h4&0g@=a2u8&!r0w@e1f"
DEBUG = "True"
ALLOWED_HOSTS = ["127.0.0.1,localhost", "*"]
# -----------------------------
# Installed apps
# -----------------------------
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core',  # your app
    'rest_framework',
    'rest_framework.authtoken',
]

# -----------------------------
# Middleware
# -----------------------------
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# -----------------------------
# URL configuration
# -----------------------------
ROOT_URLCONF = 'SecureShare.urls'

# -----------------------------
# Templates configuration
# -----------------------------
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'core', 'templates')],  # <--- templates folder
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

# -----------------------------
# WSGI
# -----------------------------
WSGI_APPLICATION = 'SecureShare.wsgi.application'

# -----------------------------
# Database (SQLite for dev)
# -----------------------------
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# -----------------------------
# Password validation
# -----------------------------
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

# -----------------------------
# Internationalization
# -----------------------------
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# -----------------------------
# Static files (CSS, JS, images)
# -----------------------------
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'core', 'static')]  # <--- static folder

MEDIA_ROOT = BASE_DIR / "media"
MEDIA_URL = "/media/"
# -----------------------------
# Login/Logout redirects
# -----------------------------
LOGIN_REDIRECT_URL = '/'     # after login, go to dashboard
LOGOUT_REDIRECT_URL = '/login/'  # after logout, go to login page
LOGIN_URL = '/login/'

# -----------------------------
# Default primary key field type
# -----------------------------
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Encryption key for files: use env or random
# FERNET_KEY = os.getenv("FERNET_KEY") or Fernet.generate_key().decode()
FERNET_KEY = Fernet.generate_key().decode()
