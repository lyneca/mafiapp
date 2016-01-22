from django.shortcuts import render
from django.http import HttpResponse
from .models import Vote


# Create your views here.
def index(request):
    votes = Vote.objects.order_by('time')
    context = {
        'votes': votes
    }
    return render(request, 'index.html', context=context)
