from django.contrib import admin
from .models import Guide

# Register your models here.
@admin.register(Guide)
class GuideAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'slug_url', 'author', 'publish', 'category_id', 'country_id')