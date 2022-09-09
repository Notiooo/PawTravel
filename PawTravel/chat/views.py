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


class ConversationView(View):
    """
    View responsible for displaying id's of user with conversation to currently logged user
    """
    def get(self, request):
        """
        GET Request
        It returns all conversation for currently logged user
        Return format: list of lists:
        [user_id, [last_message_content, last_message_time]]
        """
        user = request.user
        if user.is_authenticated:
            messages=Message.search.get_conversation_users(user)
            for id, conversation in enumerate(messages):
                message=messages[id][1]
                message_tuple=list(messages[id])
                message_tuple[1]=[message.content, str(message.date)]
                messages[id]=tuple(message_tuple)
            return JsonResponse(list(messages), safe=False)
        else:
            return JsonResponse(status=403, data={'message': "You must be logged in to access this endpoint"})


class ChatAPIView(View):
    """
    View responsible for sending and fetching messages within given conversation
    IMPORTANT: Timestamp means in class methods last message id.
    Usage of ids reduce problem of datetime conversion, timezone issues etc.
    """
    def post(self, request, receiver, content, timestamp=None):
        """
        Send new message
        Returns json with new messages in conversation if provided timestamp
        """
        user = request.user
        message_receipment = CustomUser.objects.get(id=receiver)
        if user.is_authenticated:
            if user==message_receipment:
                return JsonResponse(status=400, data={'message':"You can not send message to yourself"})

            Message(content=content, sent_by=user, sent_to=message_receipment).save()
            messages=Message.search.get_conversation(user, message_receipment, timestamp) #While we send message we can use the opportunity to refresh chat
            return JsonResponse(messages, safe=False)
        else:
            return JsonResponse(status=403, data={'message': "You must be logged in to access this endpoint"})

    def get(self, request, receiver, timestamp=None):
        """
        Fetch entire conversation or only new messages if timestamp is provided
        """
        user = request.user
        if user.is_authenticated:
            message_receipment = CustomUser.objects.get(id=receiver)
            messages=Message.search.get_conversation(user, message_receipment, timestamp)
            return JsonResponse(list(messages), safe=False)
        else:
            return JsonResponse(status=403, data={'message': "You must be logged in to access this endpoint"})
