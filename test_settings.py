import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = 'test secret key'
INSTALLED_APPS = [
    'telegram_error_notifications'
]
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
TELEGRAM_BOT_TOKEN = '999999999:AAAAAAAAAAAAAAAAA_XXXXXXXXXXXXXXXXX'
TELEGRAM_BOT_PROJECT_NAME = 'Test Django Project'
TELEGRAM_BOT_NAME = 'Test Bot'
