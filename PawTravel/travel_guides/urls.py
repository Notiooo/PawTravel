from django.urls import path
from . import views

app_name='travel_guides'
urlpatterns = [
    path('', views.GuideHomepageView.as_view(), name="guides_homepage"),
    path('user/<str:username>/', views.GuideListView.as_view(), name="get_user_guides"),
    path('add/', views.GuideCreateFormView.as_view(), name="add_guide"),
    path('list/', views.GuideListView.as_view(), name='guide_list'),
    path('<int:pk>/', views.GuideDetailView.as_view(), name='guide_detail'),
    path('<slug_url>-<int:pk>/', views.GuideDetailView.as_view(), name="guide_detail"),
    path('vote/<int:pk>/<str:mode>', views.GuideVoteView.as_view(), name='guide_vote'),

]