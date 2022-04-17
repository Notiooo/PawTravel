from django.contrib import admin
from .models import Guide

# Register your models here.
@admin.register(Guide)
class GuideAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author', 'publish', 'category', 'country')
    prepopulated_fields = {'slug': ('title',)}