import pytest
from django.conf import settings

from telegram_error_notifications.models import TelegramBot


@pytest.fixture
def telegram_bot():
    bot = TelegramBot.objects.create(name='Test Bot', chat_id=540784105)
    return bot


@pytest.fixture
def get_message():
    return 'Message for testing of generation URL.'


@pytest.mark.django_db
def test_generating_of_sending_message_url(telegram_bot, get_message):
    url = telegram_bot.generate_send_message_url(message=get_message)
    base_url = 'https://api.telegram.org/bot{}/'.format(
        settings.TELEGRAM_BOT_TOKEN)
    send_message_part = 'sendmessage?chat_id={0}&text={1}&parse_mode=html'.\
        format(telegram_bot.chat_id, get_message)
    url_should_be = '{0}{1}'.format(base_url, send_message_part)
    assert url_should_be == url


@pytest.mark.django_db
def test_bot_attributes(telegram_bot):
    assert telegram_bot.name == 'Test Bot'
    assert telegram_bot.chat_id == 540784105


@pytest.mark.django_db
def test_setting_bot_attributes(telegram_bot):
    telegram_bot.name = 'Test Bot 1'
    telegram_bot.chat_id = 540784106
    telegram_bot.save()
    assert telegram_bot.name == 'Test Bot 1'
    assert telegram_bot.chat_id == 540784106
