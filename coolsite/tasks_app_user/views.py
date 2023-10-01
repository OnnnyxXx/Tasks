from django.contrib.auth.views import LoginView
from django.http import HttpResponseForbidden
from django.urls import reverse_lazy
from django.views import View

from .forms import ArticlesForm, RegisterUserForm, LoginUserForm, ProfileForm, CommentForm
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout, get_user_model

from django.contrib.auth.mixins import LoginRequiredMixin

from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.decorators import login_required

from django.views.generic.detail import DetailView

from .models import *


def tasks_home(request):
    tasks_all = Articles.objects.order_by('-data')
    context = {
        'tasks_all': tasks_all
    }
    return render(request, 'tasks_app_user/tasks_home.html', context)


# AutoDeleteTasks
# timezone.now() - timedelta(7)
# Articles.objects.all().delete()


# UpdateTasks
class TasksUpdateView(UpdateView):
    model = Articles
    template_name = 'tasks_app_user/create.html'
    form_class = ArticlesForm


# DeleteTasks
class TasksDeleteView(DeleteView):
    model = Articles
    success_url = '/tasks'
    template_name = 'tasks_app_user/delete_tasks.html'


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

    form = ArticlesForm(user=request.user)
    date = {
        'form': form,
        'error': error,

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


@login_required
def profile(request):
    user = request.user
    profile = user.profile if hasattr(user, 'profile') else None  # Проверяем наличие профиля

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('user_home')
    else:
        form = ProfileForm(instance=profile, user=user)  # Передача пользователя в форму

    context = {'form': form}
    return render(request, 'tasks_app_user/profile.html', context)


def User_View(request):
    profile = request.user.profile
    reviews = Comment.objects.filter(profile=profile).order_by('-created_at')

    form = ProfileForm(instance=profile)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('user_home')

    context = {'form': form, 'reviews': reviews}

    return render(request, 'tasks_app_user/home_user.html', context)


def user_profile(request, username):
    user = get_object_or_404(User, username=username)
    profile = user.profile
    reviews = Comment.objects.filter(profile=profile).order_by('-created_at')

    form = ProfileForm(instance=profile)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('user_home')

    context = {'form': form, 'profile': profile, 'reviews': reviews}

    return render(request, 'tasks_app_user/user_profile.html', context)


def AddCommentView(request, username):
    user = get_object_or_404(User, username=username)

    if request.method == 'POST':
        form = CommentForm(request.POST)

        if form.is_valid():
            author = request.user
            profile = user.profile  # Get the profile of the user being reviewed
            content = form.cleaned_data['content']
            stars = form.cleaned_data['stars']
            Comment.objects.create(author=author, profile=profile, content=content, stars=stars)
            return redirect('user_profile', user.username)

    else:
        form = CommentForm()

    return render(request, 'tasks_app_user/user_reviews.html', {'form': form, 'user': user})
