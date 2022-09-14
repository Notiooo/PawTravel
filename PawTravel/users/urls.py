from django.contrib.auth.views import LoginView
from django.urls import path, include

from . import views

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('<int:pk>/', views.ProfileView.as_view(), name='profile'),
    path('<int:pk>/activites/', views.ProfileActivitiesView.as_view(), name='profile_activities'),
    path('social-auth/', include('social_django.urls', namespace='social')),
    path('<int:pk>/edit_profile/', views.EditProfileView.as_view(), name='edit_profile'),
    path('<int:pk>/manage_profile/', views.ManageProfileView.as_view(), name='manage_profile')
]
