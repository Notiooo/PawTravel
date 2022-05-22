from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, FormView, CreateView

from .forms import GuideForm
from .models import Guide
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# Create your views here.
class GuideListView(ListView):
    """
    Guide List view. It shows list of guides.
    If url has format /guides/user/<value> It will return list of guides of user with value username
    """
    model = Guide
    paginate_by = 1
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
            queryset= queryset.filter(author=self.kwargs['username'])
        return queryset


class GuideDetailView(DetailView):
    """
    Guide detail view shows details of given guide
    """
    model = Guide

class GuideFormView(CreateView):
    """
    View responsible for rendering and handling Guide creation form
    """
    template_name = "travel_guides/form.html"
    model = Guide
    fields = ['title', 'description', 'category', 'country', 'body', 'author']
