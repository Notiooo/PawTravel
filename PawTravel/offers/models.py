from django.db import models
from django.conf import settings
from tinymce.models import HTMLField


class OfferCategory(models.Model):
    name = models.CharField(max_length=100)


class Offer(models.Model):
    title = models.CharField(max_length=100)
    content = HTMLField()
    category = models.ForeignKey(OfferCategory, on_delete=models.CASCADE, related_name='category')
    image = models.ImageField(blank=False)
    datePosted = models.DateTimeField(auto_now_add=True)
    offerEnds = models.DateTimeField()
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    originalPrice = models.FloatField()
    offerPrice = models.FloatField()
    link = models.URLField()
