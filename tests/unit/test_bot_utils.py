import pytest

from telegram_error_notifications.utils import get_parameters


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


def test_getting_of_proper_parameters(get_proper_request):
    assert get_parameters(get_proper_request) == ('some_command', 540784105)


def test_getting_of_parameters_without_message(get_request_without_message):
    assert get_parameters(get_request_without_message) is None


def test_getting_of_parameters_without_chat(get_request_without_chat):
    assert get_parameters(get_request_without_chat) is None


def test_getting_of_parameters_without_request():
    assert get_parameters(b'') is None

