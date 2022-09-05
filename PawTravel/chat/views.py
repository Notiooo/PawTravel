import datetime
import time

from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import render
from django.conf import settings

# Create your views here.
from django.views import View
from .models import Message
from users.models import CustomUser


class ConversationView(LoginRequiredMixin, View):
    """
    View responsible for displaying id's of user with conversation to currently logged user
    """
    def get(self, request):
        user = request.user
        if user.is_authenticated:
            messages=Message.search.getConversationUsers(user)
            return JsonResponse(list(messages), safe=False)


class ChatAPIView(LoginRequiredMixin, View):
    """
    View responsible for sending and fetching messages within given conversation
    """
    def post(self, request, receiver, content, timestamp=None):
        user = request.user
        message_receipment = CustomUser.objects.get(id=receiver)
        if user.is_authenticated:
            if user==message_receipment:
                return JsonResponse(status=400, data={'message':"You can not send message to yourself"})

            m=Message(content=content, sent_by=user, sent_to=message_receipment)
            m.save()
            messages=Message.search.getConversation(user, message_receipment)
            return JsonResponse(messages, safe=False)  # or JsonResponse({'data': data})

    def get(self, request, receiver, timestamp=None):
        user = request.user
        if user.is_authenticated:
            message_receipment = CustomUser.objects.get(id=receiver)
            messages=Message.search.getConversation(user, message_receipment, timestamp)
            return JsonResponse(list(messages), safe=False)