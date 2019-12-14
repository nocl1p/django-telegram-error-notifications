import json
import requests
from django.conf import settings

telegram_api_url = "https://api.telegram.org/bot"


def get_parameters(body):
    if body:
        data = json.loads(body)
        message = data.get('message', None)
        if message is None:
            return None

        text = message.get('text', '')
        if isinstance(text, str):
            text = text.strip().lower()
            text = text.lstrip("/")

        chat = message.get('chat', None)
        if chat is None:
            return None
        chat_id = chat.get('id', None)

        return text, chat_id


def send_message(message, chat_id):
    data = {"chat_id": chat_id, "text": message, "parse_mode": "html"}
    return requests.post(
        '{0}{1}/sendMessage'.format(
            telegram_api_url, settings.TELEGRAM_BOT_TOKEN), data=data)


def generate_web_hook_url():
    token = settings.TELEGRAM_BOT_TOKEN
    web_hook_url = settings.TELEGRAM_BOT_WEBHOOK_URL
    if token and web_hook_url:
        url = 'https://api.telegram.org/bot{0}/setWebhook?url={1}'.format(
            token, web_hook_url
        )
        return url


def generate_log_about_creation(bot_name, created=False):
    if created:
        return 'You have created bot "{}"'.format(bot_name)
    return 'Bot was not created. ' \
           'You already have bot with the same name "{}"'.format(bot_name)


def generate_log_about_web_hook(request):
    if request:
        status = request.status_code
        if status == 200:
            content = request.json()
            message_tuple = (
                'Setting webhook status: 200 OK',
                'Description: {0}'.format(content.get('description'))
            )
            return '\n'.join(message_tuple), False
        return 'Something went wrong during setting up a webhook', True
    return 'Request was not sent by requests lib', True


def get_exception_type(message):
    if isinstance(message, str):
        if not len(message):
            raise ValueError('The message should not be empty')

        for line in message.splitlines():
            if 'Exception Type' in line:
                caption, exc_type = line.split(':')
                exc, at = exc_type.split(' at ')
                return exc.strip()

    raise ValueError('The message should be a string')
