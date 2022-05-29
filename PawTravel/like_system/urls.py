from django.urls import path
from . import views
from . conf import LIKES_OBJS
from . models import LikeSystem
from travel_guides.models import Guide

urlpatterns = [
    path('Guide/<pk>/like', views.LikeSystemView.as_view(model=Guide, action_type=LikeSystem.LIKE)),
    path('Guide/<pk>/dislike', views.LikeSystemView.as_view(model=Guide, action_type=LikeSystem.DISLIKE)),

]