from django.shortcuts import render, get_object_or_404
from .models import Guide
# Create your views here.
def guide_list(request):
    guides = Guide.objects.all()
    return render(request,
                   'guide/list.html',
                   {'guides': guides})

def guide_detail(request, year, month, day, guide):
    guide =get_object_or_404(Guide, slug=guide, publish__year=year, publish__month=month, publish__day=day)

    return render(request,
                  'guide/detail.html', {'guide': guide})