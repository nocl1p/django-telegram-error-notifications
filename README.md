# Django Telegram Error Notifications

At first you have to register your bot first before using it. 
Go to the [BotFather](https://telegram.me/BotFather) or find it in telegram, 
then create new bot by sending the `/newbot` command. 
Follow the steps until you get the username and token for your bot. 

Add application to your `INSTALLED_APPS`:
```python
INSTALLED_APPS = [
    ...,
    'telegram_error_notifications.apps.TelegramErrorNotificationsConfig'
]
```

After this you should apply migrations:
```bash
python manage.py migrate
```
By this action you will add two new models `Telegram Bot` and `Error Messages`.

Then add to the `settings.py` settings for your telegram bot:
```python
TELEGRAM_BOT_NAME = '<Your Bot Name>'
TELEGRAM_BOT_TOKEN = '<Your Bot Token>'
# If you override BotView and set up another URL provide your URL
# Also you can use ngrok utility when you work on local server. 
# Perform `ngrok http 8000` and take URL with https. For example:
# TELEGRAM_BOT_WEBHOOK_URL = https://0adb2add.ngrok.io/bot/web-hook/
# Whenever you change this variable don't forget to perform 
# `python manage.py create_telegram_bot` to reassign a webhook
TELEGRAM_BOT_WEBHOOK_URL = 'https://<your-domain>/bot/web-hook/'
TELEGRAM_BOT_PROJECT_NAME = '<Name of the current project>'
TELEGRAM_BOT_ALLOW_SEND_IN_DEBUG_MODE = False
```
- `TELEGRAM_BOT_NAME` - Name of your bot that will be used for creating it into a database
- `TELEGRAM_BOT_TOKEN` - Token that was given to you when you created your bot
- `TELEGRAM_BOT_WEBHOOK_URL` - This url will receive requests from your bot
- `TELEGRAM_BOT_PROJECT_NAME` - This variable is necessary to provide your project name when the error will be sent to your bot
- `TELEGRAM_BOT_ALLOW_SEND_IN_DEBUG_MODE` - If you want to send errors to your bot in `DEBUG` mode switch this variable to `True`

Then you should specify url in your `urls.py`:
```python
from django.urls import path, include

urlpatterns = [
    ...,
    path('bot/', include('telegram_error_notifications.urls')),
]
```

To create a bot into a database and create a webhook for it just use the management command:
```bash
python manage.py create_telegram_bot
```
This command will use `TELEGRAM_BOT_NAME` variable to create a bot

**You should necessarily send from your bot any command. 
It's necessary for getting `chat_id` and saving it to database.
Make sure you did it.**
For example you can send `/start` command. You will get `I don't know this command`.
Don't worry. After this command your bot chat_id will be saved into a database.

You can add new commands for your bot. For example, you want to add `/start` command.
Your view that will be responsible for handling telegram commands can be like this:
```python
from telegram_error_notifications.utils import send_message
from telegram_error_notifications.views import BotView


class MyBotView(BotView):
    def handle_command_start(self):
        if self.bot and self.bot.chat_id:
            message = "<b>I started working</b>"
            return send_message(message, self.bot.chat_id)
```
To handle your own command you should create `handle_command_<command>` method.