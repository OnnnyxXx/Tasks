from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views import View

from .forms import ArticlesForm
from user_profile.forms import Profile
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User


from django.contrib.auth.mixins import LoginRequiredMixin

from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.decorators import login_required

from django.views.generic.detail import DetailView
from django.utils.decorators import method_decorator
from django.http import Http404
from django.db.models import Avg
from django.db.models import Count
from .models import *


def tasks_home(request):
    category = request.GET.get('category')  # Получаем категорию из параметра запроса

    unique_cities = Profile.objects.values_list('city', flat=True).distinct()

    if category:
        tasks_all = Articles.objects.filter(category__name=category).order_by('-data')
    else:
        tasks_all = Articles.objects.order_by('-data')

    unique_cities = [city for city in unique_cities if city is not None]
    categories = Category.objects.all()

    context = {
        'tasks_all': tasks_all,
        'unique_cities': unique_cities,
        'categories': categories,
    }
    return render(request, 'tasks_app_user/tasks_home.html', context)


def category(request):
    categories = Category.objects.all().annotate(task_count=Count('articles'))
    tasks_all = Articles.objects.order_by('-data')
    context = {
        'categories': categories,
        'tasks_all': tasks_all,

    }

    return render(request, 'tasks_app_user/category.html', context)


# AutoDeleteTasks
# timezone.now() - timedelta(7)
# Articles.objects.all().delete()


# UpdateTasks
@method_decorator(login_required, name='dispatch')
class TasksUpdateView(UpdateView):
    model = Articles
    template_name = 'tasks_app_user/create.html'
    form_class = ArticlesForm

    def dispatch(self, request, *args, **kwargs):
        article = self.get_object()

        if article.author != self.request.user:
            return redirect("category")

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        article = form.save(commit=False)
        article.category = form.cleaned_data['category']
        article.save()
        return redirect('category')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


# DeleteTasks
@method_decorator(login_required, name='dispatch')
class TasksDeleteView(DeleteView):
    model = Articles
    success_url = reverse_lazy('category')  # Replace with your desired URL
    template_name = 'tasks_app_user/delete_tasks.html'

    def dispatch(self, request, *args, **kwargs):
        # Get the article object
        Articles = self.get_object()

        # Check if the current user is the owner of the article
        if Articles.author != self.request.user:
            return redirect("category")

        return super().dispatch(request, *args, **kwargs)


class TasksDetailView(DetailView, LoginRequiredMixin):
    model = Articles
    template_name = 'tasks_app_user/details_tasks.html'
    context_object_name = 'article'
    raise_exception = True


def create(request):
    error = ''
    categories = Category.objects.all()

    if request.method == 'POST':
        form = ArticlesForm(request.POST)
        if form.is_valid():

            selected_category_id = request.POST.get('category')
            article = form.save(commit=False)
            article.category_id = selected_category_id
            article.save()

            return redirect('category')

        else:
            error = 'Форма была неверной'

    form = ArticlesForm(user=request.user)
    date = {
        'form': form,
        'error': error,
        'categories': categories
    }

    return render(request, 'tasks_app_user/create.html', date)



