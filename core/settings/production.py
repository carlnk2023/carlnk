from .base import *

DEBUG = True

ALLOWED_HOSTS = ['carlnk.co', 'www.carlnk.co']

# DATABASE
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.getenv('DATABASE_NAME'),
        'USER': os.getenv('DATABASE_USER'),
        'PASSWORD': os.getenv('DATABASE_PASSWORD'),
        'HOST': os.getenv('DATABASE_HOST'),
        'PORT': os.getenv('DATABASE_PORT'),
    }
}


# Media and staticfiles boto
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_STORAGE_BUCKET_NAME')
AWS_DEFAULT_ACL = 'public-read'
AWS_S3_ENDPOINT_URL = 'https://sgp1.digitaloceanspaces.com'
AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'max-age=86400'}
# static settings
AWS_LOCATION = 'static'
STATIC_URL = f'https://{AWS_S3_ENDPOINT_URL}/{AWS_LOCATION}/'
STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
# public media settings
AWS_MEDIA_LOCATION = 'media'
PUBLIC_MEDIA_LOCATION = 'media'
MEDIA_URL = f'https://{AWS_S3_ENDPOINT_URL}/{PUBLIC_MEDIA_LOCATION}/'
DEFAULT_FILE_STORAGE = 'core.custom_storages.MediaStorage'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]


# HTTPS settings
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
CSRF_TRUSTED_ORIGINS = ['https://carlnk.co', 'https://www.carlnk.co']



# HSTS settings
SECURE_HSTS_SECONDS = 31536000 # 1 year
SECURE_HSTS_PRELOAD = True
SECURE_HSTS_INCLUDE_SUBDOMAINS = True


# STRIPE APIs
SENDGRID_API_KEY = os.getenv('SENDGRID_API_LIVE_KEY')
