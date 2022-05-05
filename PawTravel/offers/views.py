from django.shortcuts import render

from django.views.generic import DetailView
from django.views.generic import ListView
from . import models


class OfferDetailView(DetailView):
    model = models.Offer
    context_object_name = 'offer'
    template_name = 'detailed_offer.html'

class HomePageView(ListView):
    model = models.Offer
    context_object_name = 'offer'
    template_name = 'home.html'
