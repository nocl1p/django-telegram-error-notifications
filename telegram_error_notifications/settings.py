from copy import deepcopy

from django.conf import settings

from django.utils.log import DEFAULT_LOGGING


TELEGRAM_LOGGING = deepcopy(DEFAULT_LOGGING)

ALLOW_DEBUG = settings.TELEGRAM_BOT_ALLOW_SEND_IN_DEBUG_MODE

TELEGRAM_LOGGING.get('handlers').update(**{
    'telegram': {
        'level': 'ERROR',
        'filters': ['require_debug_false'] if not ALLOW_DEBUG else None,
        'class': 'telegram_error_notifications.handlers.TelegramHandler'
    }
})

TELEGRAM_LOGGING\
    .get('loggers')\
    .get('django')\
    .get('handlers')\
    .append('telegram')

setattr(settings, 'LOGGING', TELEGRAM_LOGGING)
