import requests
from django.conf import settings
from django.db import models
from django.urls import reverse

TOKEN = settings.TELEGRAM_BOT_TOKEN
BASE_URL = 'https://api.telegram.org/bot{}/'.format(TOKEN)


class TelegramBot(models.Model):
    name = models.CharField(max_length=100)
    chat_id = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return '{0}: {1}'.format(self.name, self.chat_id)

    def generate_send_message_url(self, message):
        send_message_url_part = \
            'sendmessage?chat_id={chat_id}&text={message}&parse_mode=html'

        url = '{0}{1}'.format(
            BASE_URL.format(token=TOKEN),
            send_message_url_part.format(chat_id=self.chat_id, message=message)
        )

        return url

    def send_message(self, message=''):
        if message:
            return requests.get(url=self.generate_send_message_url(message))

    class Meta:
        verbose_name = 'Telegram Bot'
        verbose_name_plural = 'Telegram Bot'


class ErrorMessage(models.Model):
    hash = models.UUIDField()
    exc_type = models.CharField(max_length=512, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    traceback = models.TextField()

    def get_absolute_url(self):
        return reverse('error_detail', args=[self.hash])

    class Meta:
        verbose_name = 'Error Message'
        verbose_name_plural = 'Error Messages'

