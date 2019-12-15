import pytest

from telegram_error_notifications.utils import get_parameters, \
    get_exception_type


@pytest.fixture
def get_proper_request():
    request = b'{"update_id":678016729,"message":{"message_id":78,"from":{' \
        b'"id":540784105,"is_bot":false,"first_name":"Test",' \
        b'"last_name":"Name","username":"test_name","language_code":"ru"},' \
        b'"chat":{"id":540784105,"first_name":"Test","last_name":"Name",' \
        b'"username":"test_name","type":"private"},"date":1576007419,' \
        b'"text":"/some_command","entities":[{"offset":0,"length":5,' \
        b'"type":"bot_command"}]}}'
    return request


@pytest.fixture
def get_request_without_message():
    return b'{"update_id":678016729}'


@pytest.fixture
def get_request_without_chat():
    request = b'{"update_id":678016729,"message":{"message_id":78,"from":{' \
        b'"id":540784105,"is_bot":false,"first_name":"Test",' \
        b'"last_name":"Name","username":"test_name","language_code":"ru"},' \
        b'"date":1576007419, "text":"/some_command","entities":[{"offset":0,' \
        b'"length":5, "type":"bot_command"}]}}'
    return request


@pytest.fixture
def telegram_error_message():
    return '''Test Project for Bot. Internal Server Error: /

Request Method: GET
Request URL: http://localhost:8000/
Django Version: 2.2
Python Version: 3.8.0
Server time: Sun, 15 Dec 2019 11:23:42  0000

Exception Type: ValueError at /

Details URL: http://localhost:8000/bot/errors/805a34b6-e8cf-48a7-b025-aa378e445779/'''


def test_getting_of_proper_parameters(get_proper_request):
    assert get_parameters(get_proper_request) == ('some_command', 540784105)


def test_getting_of_parameters_without_message(get_request_without_message):
    assert get_parameters(get_request_without_message) is None


def test_getting_of_parameters_without_chat(get_request_without_chat):
    assert get_parameters(get_request_without_chat) is None


def test_getting_of_parameters_without_request():
    assert get_parameters(b'') is None


def test_getting_of_exception_type(telegram_error_message):
    assert get_exception_type(telegram_error_message) == 'ValueError'
