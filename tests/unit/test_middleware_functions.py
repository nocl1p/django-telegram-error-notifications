import pytest
from django.conf import settings

from telegram_error_notifications.utils import format_tb, create_message


@pytest.fixture
def get_raw_traceback():
    return '''Traceback (most recent call last):
  File "/home/user/.virtualenvs/telegram_notice_error/lib/python3.8/site-packages/django/core/handlers/exception.py", line 34, in inner
    response = get_response(request)
  File "/home/user/.virtualenvs/telegram_notice_error/lib/python3.8/site-packages/django/core/handlers/base.py", line 116, in _get_response
    response = self.process_exception_by_middleware(e, request)
  File "/home/user/.virtualenvs/telegram_notice_error/lib/python3.8/site-packages/django/core/handlers/base.py", line 114, in _get_response
    response = wrapped_callback(request, *callback_args, **callback_kwargs)
  File "/home/user/PycharmProjects/telegram_notice_error/telegram_error_notifications/views.py", line 18, in home
    x = 1 / 0
ZeroDivisionError: division by zero'''


@pytest.fixture
def get_message():
    return '''Project: <b>{}</b>

<b>File "/home/user/.virtualenvs/telegram_notice_error/lib/python3.8/site-packages/django/core/handlers/exception.py"</b>
line 34, in inner
response = get_response(request)

<b>File "/home/user/.virtualenvs/telegram_notice_error/lib/python3.8/site-packages/django/core/handlers/base.py"</b>
line 116, in _get_response
response = self.process_exception_by_middleware(e, request)

<b>File "/home/user/.virtualenvs/telegram_notice_error/lib/python3.8/site-packages/django/core/handlers/base.py"</b>
line 114, in _get_response
response = wrapped_callback(request, *callback_args, **callback_kwargs)

<b>File "/home/user/PycharmProjects/telegram_notice_error/telegram_error_notifications/views.py"</b>
line 18, in home
x = 1 / 0

<i>ZeroDivisionError: division by zero</i>'''.format(settings.TELEGRAM_BOT_PROJECT_NAME)


@pytest.fixture
def get_traceback():
    return '''File "/home/user/.virtualenvs/telegram_notice_error/lib/python3.8/site-packages/django/core/handlers/exception.py", line 34, in inner
    response = get_response(request)
  File "/home/user/.virtualenvs/telegram_notice_error/lib/python3.8/site-packages/django/core/handlers/base.py", line 116, in _get_response
    response = self.process_exception_by_middleware(e, request)
  File "/home/user/.virtualenvs/telegram_notice_error/lib/python3.8/site-packages/django/core/handlers/base.py", line 114, in _get_response
    response = wrapped_callback(request, *callback_args, **callback_kwargs)
  File "/home/user/PycharmProjects/telegram_notice_error/telegram_error_notifications/views.py", line 18, in home
    x = 1 / 0
ZeroDivisionError: division by zero'''


@pytest.fixture
def get_formatted_traceback():
    return '''<b>File "/home/user/.virtualenvs/telegram_notice_error/lib/python3.8/site-packages/django/core/handlers/exception.py"</b>
line 34, in inner
response = get_response(request)
<b>File "/home/user/.virtualenvs/telegram_notice_error/lib/python3.8/site-packages/django/core/handlers/base.py"</b>
line 116, in _get_response
response = self.process_exception_by_middleware(e, request)
<b>File "/home/user/.virtualenvs/telegram_notice_error/lib/python3.8/site-packages/django/core/handlers/base.py"</b>
line 114, in _get_response
response = wrapped_callback(request, *callback_args, **callback_kwargs)
<b>File "/home/user/PycharmProjects/telegram_notice_error/telegram_error_notifications/views.py"</b>
line 18, in home
x = 1 / 0
<i>ZeroDivisionError: division by zero</i>'''


def test_formatting_of_traceback(get_traceback, get_formatted_traceback):
    tb = format_tb(get_traceback)
    assert get_formatted_traceback == ''.join(tb)


@pytest.mark.django_db
def test_creating_of_message(get_raw_traceback, get_message):
    tb = create_message(get_raw_traceback)
    assert get_message == ''.join(tb)
