from django.contrib.auth.views import LoginView
from django.urls import path, include

from . import views
from .views import ConversationView, ChatAPIView

urlpatterns = [
    path('inbox/', ConversationView.as_view(), name='inbox'),
    path('conversation/<int:receiver>', ChatAPIView.as_view(), name='send'),
    path('conversation/<int:receiver>/<int:timestamp>', ChatAPIView.as_view(), name='send'),
]
