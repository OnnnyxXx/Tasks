from django.db.models import Avg
from django.shortcuts import render, redirect
from django.views.generic import DetailView

from tasks_app_user.models import Profile


def index(request):
    profiles = Profile.objects.annotate(avg_rating=Avg('comment__stars')).order_by('-avg_rating')
    return render(request, 'tasks_app/index.html', {'profiles': profiles})


def about(reqeust):
    return render(reqeust, 'tasks_app/about.html')








