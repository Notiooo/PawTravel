from django.urls import path

from .views import OfferDetailView
from .views import HomePageView
from .views import OfferCreateView
from .views import OfferUpdateView

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('<int:pk>/edit/', OfferUpdateView.as_view(), name="offer_edit"),
    path('new/', OfferCreateView.as_view(), name='offer_new'),
    path('<int:pk>/', OfferDetailView.as_view(), name="offer"),
    path('<slug_url>-<int:pk>/', OfferDetailView.as_view(), name="offer"),
]
