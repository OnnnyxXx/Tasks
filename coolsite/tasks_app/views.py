from django.db.models import Avg
from django.shortcuts import render, redirect
from django.views.generic import DetailView, TemplateView
from rest_framework import viewsets
from user_profile.models import Profile


# class TopUsersViewSet(viewsets.ReadOnlyModelViewSet):
#     queryset = Profile.objects.annotate(avg_rating=Avg('comment__stars')).order_by('-avg_rating')
#     serializer_class = ProfileSerializer

def index(request):
    profiles = Profile.objects.annotate(avg_rating=Avg('comment__stars')).order_by('-avg_rating')
    best_profiles = profiles.filter(avg_rating__gt=3.5)
    return render(request, 'tasks_app/index.html', {'best_profiles': best_profiles})


# def index(request):
#     return render(request, 'tasks_app/index.html')

def about(reqeust):
    return render(reqeust, 'tasks_app/about.html')


class ServiceWorkerView(TemplateView):
    template_name = 'serviceworker.js'
    content_type = 'application/javascript'
    name = 'serviceworker.js'
