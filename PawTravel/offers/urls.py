from django.urls import path

from .views import OfferDetailView, OfferFormView

urlpatterns = [
    path('<int:pk>/', OfferDetailView.as_view(), name="offer"),
    path('<slug_url>-<int:pk>/', OfferDetailView.as_view(), name="offer"),
    path('add/', OfferFormView.as_view(), name="offer_form"),
]
