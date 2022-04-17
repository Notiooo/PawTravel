from django.urls import path
from . import views

app_name='travel_guides'
urlpatterns = [
    path('', views.guide_list, name='guide_list'),
    path('<int:year>/<int:month>/<int:day>/<slug:guide>/',
         views.guide_detail,
         name='guide_detail'),
]