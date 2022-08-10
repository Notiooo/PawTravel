from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from tinymce.models import HTMLField

from comments.models import Comment
from comments.forms import CommentForm


class OfferCategory(models.Model):
    """Category of individual offer such as hotels or flights"""

    name = models.CharField(max_length=100)
    icon_image = models.ImageField(blank=True)

    def __str__(self):
        return self.name


class Offer(models.Model):
    """All fields needed for a single, individual offer"""

    title = models.CharField(max_length=100)
    slug_url = models.SlugField(editable=False)
    short_content = models.TextField(max_length=300, blank=True)
    content = HTMLField()
    category = models.ForeignKey(OfferCategory, on_delete=models.CASCADE, related_name='category')
    image = models.ImageField(blank=False)
    date_posted = models.DateTimeField(auto_now_add=True)
    offer_ends = models.DateTimeField()
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    original_price = models.FloatField()
    offer_price = models.FloatField()
    link = models.URLField()
    comments = GenericRelation(Comment, related_query_name='all_comments', blank=True)

    def __str__(self):
        return self.title

    def save(self, **kwargs):
        self.slug_url = slugify(self.title)
        super(Offer, self).save(kwargs)

    def get_absolute_url(self):
        return reverse('offer', kwargs={'pk': self.pk, 'slug_url': self.slug_url})
