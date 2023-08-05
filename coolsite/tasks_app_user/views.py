import time

from django.contrib.auth.views import LoginView
from django.http import HttpResponseForbidden
from django.urls import reverse_lazy


from .forms import ArticlesForm, RegisterUserForm, LoginUserForm
from django.views.generic import DetailView, CreateView, UpdateView

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Articles

from django.utils import timezone
from datetime import timedelta


def tasks_home(request):
    tasks_all = Articles.objects.order_by('-data')
    return render(request, 'tasks_app_user/tasks_home.html', {"tasks_all": tasks_all})
timezone.now() - timedelta(1)
Articles.objects.all().delete()


class TasksDetailView(DetailView, LoginRequiredMixin):
    model = Articles
    template_name = 'tasks_app_user/details_tasks.html'
    context_object_name = 'article'
    raise_exception = True


def create(request):
    error = ''
    if request.method == 'POST':
        form = ArticlesForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('tasks_home')

        else:
            error = 'Форма была неверной'

    form = ArticlesForm()
    date = {
        'form': form,
        'error': error
    }

    return render(request, 'tasks_app_user/create.html', date)


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'tasks_app_user/register.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return dict(list(context.items()))

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'tasks_app_user/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return dict(list(context.items()))

    def get_success_url(self):
        return reverse_lazy('home')


def logout_user(request):
    logout(request)
    return redirect('login')




