from copy import deepcopy

from django.conf import settings

from django.utils.log import DEFAULT_LOGGING


telegram_logging = deepcopy(DEFAULT_LOGGING)

allow_debug = settings.TELEGRAM_BOT_ALLOW_SEND_IN_DEBUG_MODE

telegram_logging.get('handlers').update(**{
    'telegram': {
        'level': 'ERROR',
        'filters': ['require_debug_false'] if not allow_debug else None,
        'class': 'telegram_error_notifications.handlers.TelegramHandler'
    }
})

telegram_logging\
    .get('loggers')\
    .get('django')\
    .get('handlers')\
    .append('telegram')

setattr(settings, 'LOGGING', telegram_logging)
