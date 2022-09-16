from django import forms
from . import models


class OfferForm(forms.Form):
    model = models.Offer
    fields = ('title', 'description', 'price', 'image', 'category', 'offer_ends')
