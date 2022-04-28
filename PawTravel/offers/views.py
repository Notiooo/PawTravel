from django.shortcuts import render

from django.views.generic import DetailView
from . import models


class OfferDetailView(DetailView):
    model = models.Offer
    context_object_name = 'offer'
    template_name = 'detailed_offer.html'
