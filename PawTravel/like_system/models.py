from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import (
    GenericForeignKey,
    GenericRelation,
)
#from . conf import LIKE_TARGET_MODEL

USER = get_user_model()


# Create your models here.
class LikesTarget(models.Model):
    likesystem = GenericRelation("LikeSystem",
                                 related_query_name="likes_target")


class LikeSystemManager(models.Manager):
    use_for_related_fields = True

    def likes(self):
        # Забираем queryset с записями больше 0
        return self.get_queryset().filter(action__gt=0)

    def dislikes(self):
        # Забираем queryset с записями меньше 0
        return self.get_queryset().filter(action__lt=0)

    def total(self):
        # Разница между лайками и дизлайками
        likes = self.get_queryset().filter(action__gt=0)
        dislikes = self.get_queryset().filter(action__lt=0)
        result = len(likes) - len(dislikes)
        if result < 0:
            result = 0
        return result


class LikeSystem(models.Model):

    LIKE = 1
    DISLIKE = -1

    ACTIONS = ((DISLIKE, "dislike"), (LIKE, "like"))

    action = models.SmallIntegerField(choices=ACTIONS)

    user = models.ForeignKey(USER, on_delete=models.CASCADE)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)

    object_id = models.CharField(max_length=1024)

    content_object = GenericForeignKey()

    objects = LikeSystemManager()

    class Meta:
        ordering = ["-id"]
        verbose_name = "like/dislike"
        verbose_name_plural = "likes/dislikes"
