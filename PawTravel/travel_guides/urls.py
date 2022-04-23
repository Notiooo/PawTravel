from django.urls import path
from . import views

app_name='travel_guides'
urlpatterns = [
    path('', views.guide_list, name='guide_list'),
    path('<int:year>/<int:month>/<int:day>/<slug:guide>/',
         views.guide_detail,
         name='guide_detail'),
    path('user/<str:username>/',
         views.get_user_guides,
         name="get_user_guides"),
    path('add/',
         views.add_guide_view,
         name="add_guide_view"),
]