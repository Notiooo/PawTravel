from django.urls import path

from .views import OfferDetailView

urlpatterns = [
    path('<int:pk>/', OfferDetailView.as_view(), name="offer"),
    path('<slug_url>-<int:pk>/', OfferDetailView.as_view(), name="offer"),
]
