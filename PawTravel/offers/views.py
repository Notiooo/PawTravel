from django.shortcuts import render

from django.views.generic import DetailView
from . import models


class OfferDetailView(DetailView):
    """A view showing one particular offer in detail."""

    model = models.Offer
    context_object_name = 'offer'
    template_name = 'offers/detailed_offer.html'
