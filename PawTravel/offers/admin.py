from django.contrib import admin
from . import models

# Register your models here.

admin.site.register(models.Offer)
admin.site.register(models.OfferCategory)