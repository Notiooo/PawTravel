from django.urls import path

from .views import OfferDetailView, OfferVoteView

urlpatterns = [
    path('<int:pk>/', OfferDetailView.as_view(), name="offer"),
    path('<slug_url>-<int:pk>/', OfferDetailView.as_view(), name="offer"),
    path('vote/<int:pk>/<str:mode>', OfferVoteView.as_view(), name='offer_vote'),

]
