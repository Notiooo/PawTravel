from django.urls import path

from .views import OfferDetailView
from .views import HomePageView
from .views import OfferCreateView

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('<int:pk>/', OfferDetailView.as_view(), name="offer"),
    path('new/', OfferCreateView.as_view(), name='offer_new')
]
