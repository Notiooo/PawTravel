from django.db import models
from django.db.models import Q
# Create your models here.
from django.conf import settings

class MessageManager(models.Manager):
    def getConversation(self, userOne, userTwo):
        """
        Get all messages between two users
        :param userOne: First user in conversation
        :param userTwo: Second user in conversation
        Please note that results are the same for a pair of users no matter in which order provided
        """
        quert_set_one= super().get_queryset().filter(sent_by=userOne, sent_to=userTwo)
        quert_set_two= super().get_queryset().filter(sent_by=userTwo, sent_to=userOne)
        result= quert_set_one | quert_set_two
        return result.order_by('date')

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
        return "{} to {} [{}]: {}".format(self.sent_by.username, self.sent_to.usernane, self.date, self.content)