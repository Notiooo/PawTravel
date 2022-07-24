from django.views.generic import ListView, DetailView, CreateView

from .forms import GuideForm
from .models import Guide
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic.edit import FormMixin
from django.views.generic.list import MultipleObjectMixin

from users.models import CustomUser
from comments.forms import CommentForm


class GuideListView(ListView):
    """
    Guide List view. It shows list of guides.
    If url has format /guides/user/<value> It will return list of guides of user with value username
    """
    model = Guide
    paginate_by = 1
    template_name = "travel_guides/guide_list.html"

    def get_queryset(self):
        category=None
        country=None
        keywords=None
        if 'category' in self.request.GET:
            category=self.request.GET['category']
        if 'country' in self.request.GET:
            category=self.request.GET['country']
        if 'keywords' in self.request.GET:
            keywords=[self.request.GET['keywords']]
        queryset=Guide.search.search(country=country, category=category, keywords=keywords)
        if 'username' in self.kwargs:
            queryset= queryset.filter(author=CustomUser.objects.get(username=self.kwargs['username']), visible='visible')
        return queryset


class GuideDetailView(FormMixin, DetailView, MultipleObjectMixin):
    """
    Guide detail view shows details of given guide
    """
    model = Guide
    template_name = "travel_guides/guide_detail.html"
    form_class = CommentForm
    paginate_by = 5

    def get_context_data(self, **kwargs):
        offer = self.get_object()
        object_list = offer.comments.all()
        return super().get_context_data(object_list=object_list, **kwargs)

    def get_queryset(self):
        return super().get_queryset().filter(visible='visible')

    def dispatch(self, request, *args, **kwargs):
        """
        The function, if slug is not specified, but a valid id is given,
        redirects to the address with the entered slug. Otherwise, it behaves in the standard way
        """
        this = self.get_object()
        if 'slug_url' not in kwargs or kwargs['slug_url'] != this.slug_url:
            return HttpResponseRedirect(reverse('travel_guides:guide_detail', kwargs={'pk': this.pk, 'slug_url': this.slug_url}))
        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('travel_guides:guide_detail', kwargs={'pk': self.get_object().id})

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
        return super(GuideDetailView, self).form_valid(form)

class GuideFormView(LoginRequiredMixin, CreateView):
    """
    View responsible for rendering and handling Guide creation form
    """
    login_url = "/users/login/"
    template_name = "travel_guides/form.html"
    model = Guide
    form_class = GuideForm

    def form_valid(self, form):
        form.instance.author=self.request.user
        return super().form_valid(form)