from django.contrib import admin
from . models import LikeSystem

# Register your models here.


class LikeSystemAdmin(admin.ModelAdmin):
    list_display = ("action", "user")


admin.site.register(LikeSystem, LikeSystemAdmin)
