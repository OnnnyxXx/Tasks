from django.shortcuts import render, redirect
from django.views.generic import DetailView


def index(request):
    return render(request, 'tasks_app/index.html')


def about(reqeust):
    return render(reqeust, 'tasks_app/about.html')








