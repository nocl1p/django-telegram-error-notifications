from django.urls import path
from django.views.decorators.csrf import csrf_exempt

import telegram_error_notifications.views as bot_views


urlpatterns = [
    path(
        'web-hook/',
        csrf_exempt(bot_views.BotView.as_view()),
        name='telegram-bot-web-hook'
    ),
    path('errors/<slug:slug>/', bot_views.error_detail, name='error_detail')
]
