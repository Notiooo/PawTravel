import datetime

import pytz
from django.db import models
from django.db.models import Q
# Create your models here.
from django.conf import settings
from itertools import chain


class MessageManager(models.Manager):
    def get_conversation(self, user_one, user_two, oldest_id=None):
        """
        Get all messages between two users
        :param user_one: First user in conversation
        :param user_two: Second user in conversation
        :param oldest_id: Optional parameter which will return conversation messages newer than the id provided
        :return: List of serialized Message objects

        Please note that results are the same for a pair of user ids no matter in which order provided
        ex. get_conversation(1,2) will return the same results as get_conversation(2,1)
        """
        if oldest_id==None:
            oldest_id=0

        quert_set_one= super().get_queryset().filter(id__gt=oldest_id, sent_by=user_one, sent_to=user_two)
        quert_set_two= super().get_queryset().filter(id__gt=oldest_id, sent_by=user_two, sent_to=user_one)
        result= quert_set_one | quert_set_two
        return list(result.order_by('date').values())

    def _get_last_message(self, user_tuple):
        """
        Fetch last message in conversation between two users
        :param user_tuple: Tuple of two users ids
        :return: Message object
        """
        quert_set_one= super().get_queryset().filter(sent_by=user_tuple[0], sent_to=user_tuple[1])
        quert_set_two= super().get_queryset().filter(sent_by=user_tuple[1], sent_to=user_tuple[0])
        result= quert_set_one | quert_set_two
        id=result.order_by('-pk')[0].id
        return super().get_queryset().get(id=id)

    def get_conversation_users(self, user):
        """
        Get all user whith whom given user have conversation
        :param user: user whose list of conversation we want
        :return: list of unique user id's which have at least one message with given user, additionally last message will be zipped with each user id
        """
        quert_set_one= super().get_queryset().filter(sent_by=user)
        q_one=quert_set_one.values_list('sent_to')
        q_one=(list(q_one))

        quert_set_two= super().get_queryset().filter(sent_to=user)
        q_two=quert_set_two.values_list('sent_by')
        q_two=(list(q_two))
        result=q_one+q_two
        result=list(chain(*result))
        res=list(dict.fromkeys(result))
        res=map(lambda e: (e, user.id), res)
        res=list(map(self._get_last_message, res))
        return list((zip(list(dict.fromkeys(result)), res)))


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