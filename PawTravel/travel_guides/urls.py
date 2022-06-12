from django.urls import path
from . import views

app_name='travel_guides'
urlpatterns = [
    path('user/<str:username>/', views.GuideListView.as_view(), name="get_user_guides"),
    path('add/', views.GuideFormView.as_view(), name="add_guide"),
    path('list/', views.GuideListView.as_view(), name='guide_list'),
    path('<int:pk>/', views.GuideDetailView.as_view(), name="guide"),
    path('<slug>-<int:pk>/', views.GuideDetailView.as_view(), name="guide"),
]