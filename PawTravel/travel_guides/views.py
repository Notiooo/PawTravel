from django.http import JsonResponse
from django.views import View
from django.views.generic import ListView, DetailView, CreateView

from .forms import GuideForm
from .models import Guide
from django.contrib.auth.mixins import LoginRequiredMixin
from users.models import CustomUser
from voting.models import Vote
# Create your views here.
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


class GuideDetailView(DetailView):
    """
    Guide detail view shows details of given guide
    """
    model = Guide
    template_name = "travel_guides/guide_detail.html"

    def get_queryset(self):
        return super().get_queryset().filter(visible='visible')

    def get_context_data(self, **kwargs):
        context = super(GuideDetailView, self).get_context_data(**kwargs)
        context["likes"] = Vote.objects.get_score(context['guide'])['score']
        context["num_votes"] = Vote.objects.get_score(context['guide'])['num_votes']
        return context



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

class GuideVoteView(View):
    """
    View responsible for processing voting system
    """
    def post(self, request, slug, mode):
        user=request.user
        guide=Guide.objects.get(slug=slug)
        if user.is_authenticated:
            if mode=="like":
                Vote.objects.record_vote(guide, user, 1)
            elif mode=="dislike":
                Vote.objects.record_vote(guide, user, -1)
            else:
                Vote.objects.record_vote(guide, user, 0)
        data=dict()
        data["likes"] = Vote.objects.get_score(guide)['score']
        data["num_votes"] = Vote.objects.get_score(guide)['num_votes']
        return JsonResponse(data)
