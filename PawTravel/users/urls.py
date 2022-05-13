from django.urls import path, include
from . import views

urlpatterns = [
    path('login/', views.auth_views.LoginView.as_view(), name='login'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('social-auth/', include('social_django.urls', namespace='social'))
]