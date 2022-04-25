from django.shortcuts import render, get_object_or_404

from .forms import GuideForm
from .models import Guide
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.
def guide_list(request):
    '''
    Retrieve all guides
    :param request: HTTP request
    :return: List of all guides
    '''

    guides_list = Guide.objects.filter()
    paginator=Paginator(guides_list, 2)

    page = request.GET.get('page')
    try:
        guides=paginator.page(page)
    except PageNotAnInteger:
        guides=paginator.page(1)
    except EmptyPage:
        guides=paginator.page(paginator.num_pages)
    #print(request.GET)
    return render(request,
                   'guide/list.html',
                   {'guides': guides,
                    'page': page})

def guide_detail(request, year, month, day, guide):
    '''
    Retrieve specific guide
    :param request: HTTP request
    :param year: year when article was published
    :param month: month when article was published
    :param day: day when article was published
    :param guide: Slug of the guide
    :return: View with given guide
    '''
    guide =get_object_or_404(Guide, slug=guide, publish__year=year, publish__month=month, publish__day=day)

    return render(request,
                  'guide/detail.html', {'guide': guide})

def get_user_guides(request, username):
    '''
    Retrieve guides writen by given user
    :param request: HTTP request
    :param username: Username of which guides will be retrieved
    :return: View with given guides
    TODO: this method must be updated when User app will be implemented
    '''
    guides = Guide.search.search_by_user(username)
    return render(request,
                   'guide/list.html',
                   {'guides': guides})

def add_guide_view(request):
    """
    View responsible for displaying and handling guide's creation form
    :param request: HTTP request
    :return: View with a form
    """
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = GuideForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            new_guide=form.save(commit=True)

    # if a GET (or any other method) we'll create a blank form
    else:
        form = GuideForm()

    return render(request, 'guide/form.html', {'form': form})