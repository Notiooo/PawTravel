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
    TODO: Add support for search queries
    """
    model = Guide
    paginate_by = 1
    def get_queryset(self):
        if 'username' in self.kwargs:
            queryset= Guide.objects.filter(author=self.kwargs['username'])
        else:
            queryset=  Guide.objects.all()
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
