from django.contrib import admin
from travel_guides import models


admin.site.register(models.Guide)
admin.site.register(models.GuideCategory)
admin.site.register(models.Country)