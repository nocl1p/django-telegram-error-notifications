import logging
import os
import uuid
from copy import copy
from pathlib import Path

from django.conf import settings
from django.db import transaction
from django.template import Context
from django.views.debug import ExceptionReporter, DEBUG_ENGINE

from telegram_error_notifications.models import TelegramBot, ErrorMessage
from telegram_error_notifications.utils import get_exception_type

APP_DIR = os.path.dirname(os.path.abspath(__file__))


class TelegramExceptionReporter(ExceptionReporter):
    def get_telegram_traceback_text(self):
        with Path(APP_DIR,
                  'templates', 'telegram_technical_500.txt').open() as fh:
            t = DEBUG_ENGINE.from_string(fh.read())

        c = Context(self.get_traceback_data(), autoescape=False, use_l10n=False)
        return t.render(c)


class TelegramHandler(logging.Handler):
    def emit(self, record):
        try:
            request = record.request
        except Exception:
            request = None

        no_exc_record = copy(record)
        no_exc_record.exc_info = None
        no_exc_record.exc_text = None

        if record.exc_info:
            exc_info = record.exc_info
        else:
            exc_info = (None, record.getMessage(), None)

        reporter = TelegramExceptionReporter(request, is_email=False, *exc_info)

        with transaction.atomic():
            err = ErrorMessage.objects.create(
                traceback=reporter.get_traceback_html(), hash=uuid.uuid4())
            protocol = 'https://' if request.is_secure() else 'http://'
            host = request.get_host()
            detail_url = '{0}{1}{2}'.format(
                protocol, host, err.get_absolute_url())
            header = '<b>{0}</b>. {1}'.format(
                settings.TELEGRAM_BOT_PROJECT_NAME or 'Unknown Project',
                self.format(no_exc_record)
            )

            message = "{0}\n{1}\n\nDetails URL: {2}".format(
                header, reporter.get_telegram_traceback_text(), detail_url)

            err.exc_type = get_exception_type(message)
            err.save()

        bot_name = settings.TELEGRAM_BOT_NAME
        try:
            bot = TelegramBot.objects.get(name=bot_name)
        except TelegramBot.DoesNotExist:
            return
        else:
            bot.send_message(message)
