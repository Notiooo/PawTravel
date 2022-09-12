from django.contrib.auth.views import LoginView
from django.urls import path, include

from . import views

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('profile_added/', views.ProfileAddedView.as_view(), name='profile_added'),
    path('profile_activities/', views.ProfileActivitiesView.as_view(), name='profile_activities'),
    path('social-auth/', include('social_django.urls', namespace='social'))
]
