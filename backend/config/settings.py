from datetime import timedelta
from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'change-me-in-production')
DEBUG = os.environ.get('DJANGO_DEBUG', 'true').lower() == 'true'
ALLOWED_HOSTS = [host for host in os.environ.get('DJANGO_ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',') if host]
render_host = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if render_host:
    ALLOWED_HOSTS.append(render_host)
INSTALLED_APPS = ['django.contrib.admin','django.contrib.auth','django.contrib.contenttypes','django.contrib.sessions','django.contrib.messages','django.contrib.staticfiles','corsheaders','rest_framework','rest_framework_simplejwt.token_blacklist','django_filters','drf_spectacular','users','products','inventory','notifications','analytics']
MIDDLEWARE = ['corsheaders.middleware.CorsMiddleware','django.middleware.security.SecurityMiddleware','django.contrib.sessions.middleware.SessionMiddleware','django.middleware.common.CommonMiddleware','django.middleware.csrf.CsrfViewMiddleware','django.contrib.auth.middleware.AuthenticationMiddleware','django.contrib.messages.middleware.MessageMiddleware','django.middleware.clickjacking.XFrameOptionsMiddleware']
ROOT_URLCONF = 'config.urls'
TEMPLATES = [{'BACKEND':'django.template.backends.django.DjangoTemplates','DIRS':[],'APP_DIRS':True,'OPTIONS':{'context_processors':['django.template.context_processors.request','django.contrib.auth.context_processors.auth','django.contrib.messages.context_processors.messages']}}]
WSGI_APPLICATION = 'config.wsgi.application'
if os.environ.get('POSTGRES_HOST') or (os.environ.get('POSTGRES_DB') and os.environ.get('USE_SQLITE', '').lower() != 'true'):
    DATABASES = {'default': {'ENGINE':'django.db.backends.postgresql', 'NAME':os.environ.get('POSTGRES_DB','foodguard'), 'USER':os.environ.get('POSTGRES_USER','foodguard'), 'PASSWORD':os.environ.get('POSTGRES_PASSWORD','foodguard'), 'HOST':os.environ.get('POSTGRES_HOST','localhost'), 'PORT':os.environ.get('POSTGRES_PORT','5432'), 'CONN_MAX_AGE':60, 'OPTIONS':{'sslmode':os.environ.get('POSTGRES_SSLMODE','prefer')}}}
else:
    DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3', 'NAME': BASE_DIR / 'db.sqlite3'}}
AUTH_PASSWORD_VALIDATORS = [{'NAME':'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},{'NAME':'django.contrib.auth.password_validation.MinimumLengthValidator','OPTIONS':{'min_length':12}},{'NAME':'django.contrib.auth.password_validation.CommonPasswordValidator'},{'NAME':'django.contrib.auth.password_validation.NumericPasswordValidator'}]
LANGUAGE_CODE='en-us'; TIME_ZONE='UTC'; USE_I18N=True; USE_TZ=True; STATIC_URL='static/'; STATIC_ROOT = BASE_DIR / 'staticfiles'; DEFAULT_AUTO_FIELD='django.db.models.BigAutoField'
AUTH_USER_MODEL = 'users.User'
REST_FRAMEWORK = {'DEFAULT_AUTHENTICATION_CLASSES': ('rest_framework_simplejwt.authentication.JWTAuthentication',), 'DEFAULT_PERMISSION_CLASSES': ('rest_framework.permissions.IsAuthenticated',), 'DEFAULT_RENDERER_CLASSES': ('rest_framework.renderers.JSONRenderer',), 'DEFAULT_PAGINATION_CLASS':'config.pagination.StandardResultsSetPagination', 'PAGE_SIZE':20, 'DEFAULT_FILTER_BACKENDS':('django_filters.rest_framework.DjangoFilterBackend','rest_framework.filters.SearchFilter','rest_framework.filters.OrderingFilter'), 'DEFAULT_SCHEMA_CLASS':'drf_spectacular.openapi.AutoSchema'}
SPECTACULAR_SETTINGS = {'TITLE':'FoodGuard API','DESCRIPTION':'Smart food safety monitoring and expiry alerts API.','VERSION':'1.0.0','SERVE_INCLUDE_SCHEMA':False}
CELERY_BROKER_URL=os.environ.get('CELERY_BROKER_URL','redis://localhost:6379/0')
CELERY_RESULT_BACKEND=os.environ.get('CELERY_RESULT_BACKEND','redis://localhost:6379/1')
CELERY_TIMEZONE=TIME_ZONE
CELERY_BEAT_SCHEDULE={'daily-expiry-reminders':{'task':'notifications.tasks.send_daily_expiry_reminders','schedule':__import__('celery.schedules',fromlist=['crontab']).crontab(hour=7,minute=0)}}
SIMPLE_JWT = {'ACCESS_TOKEN_LIFETIME': timedelta(minutes=15), 'REFRESH_TOKEN_LIFETIME': timedelta(days=7), 'ROTATE_REFRESH_TOKENS': True, 'BLACKLIST_AFTER_ROTATION': True, 'AUTH_HEADER_TYPES': ('Bearer',)}
CORS_ALLOWED_ORIGINS = [o for o in os.environ.get('CORS_ALLOWED_ORIGINS', 'http://localhost:5173,http://127.0.0.1:5173,http://localhost:3000,http://127.0.0.1:3000').split(',') if o]
if render_host:
    CORS_ALLOWED_ORIGINS.append(f'https://{render_host}')
    CORS_ALLOWED_ORIGINS.append(f'http://{render_host}')
CORS_ALLOW_ALL_ORIGINS = DEBUG
CSRF_TRUSTED_ORIGINS = [origin.replace('http://', 'https://') if origin.startswith('http://') else origin for origin in CORS_ALLOWED_ORIGINS]
EMAIL_BACKEND = os.environ.get('DJANGO_EMAIL_BACKEND','django.core.mail.backends.console.EmailBackend')
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL', 'FoodGuard <no-reply@foodguard.example>')
FRONTEND_URL = os.environ.get('FRONTEND_URL', 'http://localhost:5173')
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = not DEBUG
SESSION_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SECURE = not DEBUG
