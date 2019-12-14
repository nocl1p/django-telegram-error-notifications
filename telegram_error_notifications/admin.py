from django.contrib import admin

from telegram_error_notifications.models import TelegramBot, ErrorMessage


@admin.register(TelegramBot)
class TelegramBotAdmin(admin.ModelAdmin):
    list_display = ('name', 'chat_id')


@admin.register(ErrorMessage)
class ErrorMessageAdmin(admin.ModelAdmin):
    list_display = ('hash', 'exc_type', 'date')
    list_filter = ('date', )
