from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-50=nfh&&!yhy^9x!7*d$@#w=94i$zg)84b#mq*!pq#)&m=y99v'

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


    'rest_framework',
    'rest_framework.authtoken',
    'rest_framework_simplejwt.token_blacklist',

    'djoser',
    
    'django_celery_beat',


    'users',
    'students',
    'courses',
    'grades',
    'attendance',
    'notifications',
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

ROOT_URLCONF = 'StudentManagementSystem.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'StudentManagementSystem.wsgi.application'


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

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'









DJOSER = {
    'USER_ID_FIELD': 'id',
    'LOGIN_FIELD': 'email', 
    'SERIALIZERS': {
        'user': 'users.serializers.UserSerializer',  
        'current_user': 'users.serializers.UserSerializer',  
    },
}

AUTH_USER_MODEL = 'users.User'



REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),


    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 3,


    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.UserRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'user': '1000/day',
    },
}

SIMPLE_JWT = {
    'AUTH_HEADER_TYPES': ('JWT',),
}


CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
    }
}


CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
CELERY_TASK_ALWAYS_EAGER = False


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {  # Define the verbose formatter here
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file_grades': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'logs/grades.log',
            'formatter': 'verbose',
            'encoding': 'utf-8',
        },
        'file_attendance': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'logs/attendance.log',
            'formatter': 'verbose',
            'encoding': 'utf-8',
        },
        'file_courses': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'logs/courses.log',
            'formatter': 'verbose',
            'encoding': 'utf-8',
        },
        'file_students': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'logs/students.log',
            'formatter': 'verbose',
            'encoding': 'utf-8',
        },
        'file_users': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'logs/users.log',
            'formatter': 'verbose',
            'encoding': 'utf-8',
        },
    },
'loggers': {
        'grades': {
            'handlers': ['file_grades'],
            'level': 'INFO',
            'propagate': False,
        },
        'attendance': {
            'handlers': ['file_attendance'],
            'level': 'INFO',
            'propagate': False,
        },
        'courses': {
            'handlers': ['file_courses'],
            'level': 'INFO',
            'propagate': False,
        },
        'students': {
            'handlers': ['file_students'],
            'level': 'INFO',
            'propagate': False,
        },
        'users': {
            'handlers': ['file_users'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}


# JWT Configuration
from datetime import timedelta

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=10),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
}