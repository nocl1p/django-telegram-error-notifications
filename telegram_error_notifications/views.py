from django.conf import settings
from django.http import JsonResponse, Http404, HttpResponse
from django.views import View

from telegram_error_notifications.models import TelegramBot, ErrorMessage
from telegram_error_notifications.utils import get_parameters, send_message


class BotView(View):
    def __init__(self, **kwargs):
        """
        We will persist bot object as attribute for convenience
        """
        super().__init__(**kwargs)
        try:
            self.bot = TelegramBot.objects.get(name=settings.TELEGRAM_BOT_NAME)
        except TelegramBot.DoesNotExist:
            self.bot = None

    def post(self, request, *args, **kwargs):
        """
        Handle POST request
        """
        parameters = get_parameters(request.body)
        if parameters is None:
            return JsonResponse({}, status=400)

        text, chat_id = parameters

        if self.bot and not self.bot.chat_id:
            self.bot.chat_id = chat_id
            self.bot.save()

        self.handle_command(text)
        return JsonResponse({}, status=200)

    def handle_command(self, command):
        """
        This method tries to find a method handle_command_<command>.
        Then this method will be invoked if it is.
        """
        method_name = 'handle_command_{}'.format(command)

        if hasattr(self, method_name):
            handle_method = getattr(self, method_name)
            return handle_method()
        return self.default_command()

    def default_command(self):
        """
        Method handles commands that don't have their own handlers
        """
        if self.bot and self.bot.chat_id:
            message = '<b>I don\'t know this command</b>'
            return send_message(message, self.bot.chat_id)


def error_detail(request, slug=None):
    try:
        err = ErrorMessage.objects.get(hash=slug)
    except ErrorMessage.DoesNotExist:
        raise Http404
    else:
        html = err.traceback
        return HttpResponse(html)
