from django.shortcuts import render

from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView 
from . import models


class OfferDetailView(DetailView):
    model = models.Offer
    context_object_name = 'offer'
    template_name = 'detailed_offer.html'

class HomePageView(ListView):
    model = models.Offer
    context_object_name = 'offer'
    template_name = 'home.html'

class OfferCreateView(CreateView):
    model = models.Offer
    template_name = 'new_offer.html'
    fields = [
        'title', 'shortContent', 'content', 'category', 'image',
        'originalPrice', 'offerPrice', 'offerEnds', 'link']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)