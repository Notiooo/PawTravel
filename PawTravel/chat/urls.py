from django.contrib.auth.views import LoginView
from django.urls import path, include

from . import views
from .views import ConversationView, ChatAPIView

urlpatterns = [
    path('inbox/', ConversationView.as_view(), name='inbox'),
    path('conversation/', ChatAPIView.as_view(), name='send'),

]
