from django.http import HttpResponseRedirect
from django.urls import reverse

from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, UpdateView 
from django.views.generic import DetailView
from django.views.generic.edit import FormMixin
from django.views.generic.list import MultipleObjectMixin

from . import models
from comments.forms import CommentForm

class HomePageView(ListView):
    model = models.Offer
    context_object_name = 'offer'
    template_name = 'offers/home.html'

class OfferCreateView(CreateView):
    model = models.Offer
    template_name = 'offers/new_offer.html'
    fields = ['title', 'short_content', 'content', 'category', 'image',
        'original_price', 'offer_price', 'offer_ends', 'link']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class OfferUpdateView(UpdateView):  #Here will be mixin preventing access from different users
    model = models.Offer
    fields = [
        'title', 'short_content', 'content', 'category', 'image',
        'original_price', 'offer_price', 'offer_ends', 'link']
    template_name = 'offers/edit_offer.html'

class OfferDetailView(FormMixin, DetailView, MultipleObjectMixin):
    """A view showing one particular offer in detail."""
    model = models.Offer
    context_object_name = 'offer'
    template_name = 'offers/detailed_offer.html'
    form_class = CommentForm
    paginate_by = 5

    def get_context_data(self, **kwargs):
        offer = self.get_object()
        object_list = offer.comments.all()
        return super().get_context_data(object_list=object_list, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        this = self.get_object()
        if 'slug_url' not in kwargs or kwargs['slug_url'] != this.slug_url:
            return HttpResponseRedirect(reverse('offer', kwargs={'pk': this.pk, 'slug_url': this.slug_url}))
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('offer', kwargs={'pk': self.get_object().id})

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['form_object'] = self.get_object()
        return kwargs

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()

        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.form_valid(form, self.request)
        return super(OfferDetailView, self).form_valid(form)
