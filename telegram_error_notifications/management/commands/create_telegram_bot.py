import requests
from django.conf import settings
from django.core.management import BaseCommand

from telegram_error_notifications.models import TelegramBot
import telegram_error_notifications.utils as bot_utils


class Command(BaseCommand):
    """This command is for creating of the telegram bot in database and setting
    up of a webhook"""

    def handle(self, *args, **options):
        name = settings.TELEGRAM_BOT_NAME
        if name:
            bot, created = TelegramBot.objects.get_or_create(name=name)
            if bot:
                self.stdout.write(self.style.SUCCESS(
                    bot_utils.generate_log_about_creation(bot.name, created)))

                web_hook_url = bot_utils.generate_web_hook_url()
                if web_hook_url:
                    r = requests.get(url=web_hook_url)
                    self.stdout.write(self.style.SUCCESS(
                        'Webhook URL: {0}'.format(web_hook_url)))
                else:
                    r = None

                web_hook_message, error = \
                    bot_utils.generate_log_about_web_hook(r)
                self.stdout.write(self.style.SUCCESS(web_hook_message)) \
                    if not error else \
                    self.stderr.write(self.style.ERROR(web_hook_message))
            return

        self.stderr.write(self.style.ERROR(
            'You should provide a name of your bot in settings.py file'
        ))
