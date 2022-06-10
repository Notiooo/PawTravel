from django.http import HttpResponseRedirect
from django.urls import reverse

from django.views.generic import DetailView
from . import models


class OfferDetailView(DetailView):
    """A view showing one particular offer in detail."""

    model = models.Offer
    context_object_name = 'offer'
    template_name = 'offers/detailed_offer.html'

    def dispatch(self, request, *args, **kwargs):
        this = self.get_object()
        if 'slug_url' not in kwargs or kwargs['slug_url'] != this.slug_url:
            return HttpResponseRedirect(reverse('offer', kwargs={'pk': this.pk, 'slug_url': this.slug_url}))
        return super().dispatch(request, *args, **kwargs)
