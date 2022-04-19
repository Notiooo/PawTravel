from django.shortcuts import render, get_object_or_404
from .models import Guide
from django.utils.datastructures import MultiValueDictKeyError

# Create your views here.
def guide_list(request):
    '''
    Retrieve all guides
    :param request: HTTP request
    :return: List of all guides
    '''
    guides = Guide.objects.all()
    #print(request.GET.get('test'))
    return render(request,
                   'guide/list.html',
                   {'guides': guides})

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
    guides = Guide.objects.filter(author=username)
    return render(request,
                   'guide/list.html',
                   {'guides': guides})

