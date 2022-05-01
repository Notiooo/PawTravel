from django.db import models
from django.conf import settings
from tinymce.models import HTMLField


class OfferCategory(models.Model):
    name = models.CharField(max_length=100)
    iconImage = models.ImageField(blank=True)

    def __str__(self):
        return self.name


class Offer(models.Model):
    title = models.CharField(max_length=100)
    shortContent = models.TextField(max_length=300, blank=True)
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

    def __str__(self):
        return self.title