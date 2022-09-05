import datetime

import pytz
from django.db import models
from django.db.models import Q
# Create your models here.
from django.conf import settings
from itertools import chain


class MessageManager(models.Manager):
    def getConversation(self, userOne, userTwo, oldest_id=None):
        """
        Get all messages between two users
        :param userOne: First user in conversation
        :param userTwo: Second user in conversation
        :param oldest_id: Optional parameter which will return conversation messages newer than the id provided
        Please note that results are the same for a pair of users no matter in which order provided
        """
        if oldest_id==None:
            oldest_id=0

        quert_set_one= super().get_queryset().filter(id__gt=oldest_id, sent_by=userOne, sent_to=userTwo)
        quert_set_two= super().get_queryset().filter(id__gt=oldest_id, sent_by=userTwo, sent_to=userOne)
        result= quert_set_one | quert_set_two
        return list(result.order_by('date').values())
    def getConversationUsers(self, user):
        """
        Get all user whith whom given user have conversation
        :param user: user whose list of conversation we want
        :return: list of unique user id's which have at least one message with given user
        """
        quert_set_one= super().get_queryset().filter(sent_by=user)
        q_one=quert_set_one.values_list('sent_to')
        q_one=(list(q_one))

        quert_set_two= super().get_queryset().filter(sent_to=user)
        q_two=quert_set_two.values_list('sent_by')
        q_two=(list(q_two))
        result=q_one+q_two
        result=list(chain(*result))
        return list(dict.fromkeys(result))

class Message(models.Model):
    """
    Class representing single message
    """
    sent_by=models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="sender"
    )
    sent_to=models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="receiver"
    )
    content=models.CharField(max_length=1024)
    date=models.DateTimeField(auto_now_add=True)
    search = MessageManager()

    def __str__(self):
        return "{} to {} [{}]: {}".format(self.sent_by, self.sent_to, self.date, self.content)