from django.contrib.auth.views import LoginView
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views import View

from .forms import ArticlesForm, RegisterUserForm, LoginUserForm, ProfileForm, CommentForm, ConversationMessageForm
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout, get_user_model

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
    average_stars = reviews.aggregate(Avg('stars'))['stars__avg']

    form = ProfileForm(instance=profile)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('user_home')

    context = {'form': form, 'reviews': reviews, 'average_stars': average_stars}

    return render(request, 'tasks_app_user/home_user.html', context)


def user_profile(request, username):
    user = get_object_or_404(User, username=username)
    profile = user.profile
    reviews = Comment.objects.filter(profile=profile).order_by('-created_at')
    average_stars = reviews.aggregate(Avg('stars'))['stars__avg']
    form = ProfileForm(instance=profile)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('user_home')

    context = {'form': form, 'profile': profile, 'reviews': reviews, 'average_stars': average_stars}

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


# UpdateComment
@method_decorator(login_required, name='dispatch')
class CommentUpdateView(UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'tasks_app_user/user_reviews.html'
    success_url = reverse_lazy('user_profile')

    def dispatch(self, request, *args, **kwargs):
        # Получить объект комментария
        comment = self.get_object()

        # Проверьте, является ли текущий пользователь автором комментария
        if comment.author != self.request.user:
            return redirect("home")

        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        profile = self.object.profile
        user = profile.user
        # Redirect to the user profile page of the author of the comment
        return reverse_lazy('user_profile', kwargs={'username': user.username})


# DeleteComment

@method_decorator(login_required, name='dispatch')
class CommentDeleteView(DeleteView):
    model = Comment
    success_url = reverse_lazy('user_profile')
    template_name = 'tasks_app_user/delete_comment.html'

    def dispatch(self, request, *args, **kwargs):
        # Получить объект комментария
        comment = self.get_object()

        # Проверьте, является ли текущий пользователь автором комментария
        if comment.author != self.request.user:
            return redirect("home")

        return super().dispatch(request, *args, **kwargs)

    def get_success_url(self):
        profile = self.object.profile
        user = profile.user
        # Redirect to the user profile page of the author of the comment
        return reverse_lazy('user_profile', kwargs={'username': user.username})


@login_required
def new_conversation(request, item_pk):
    item = get_object_or_404(Articles, pk=item_pk)

    if item.author == request.user:
        return redirect('home')

    conversations = Conversation.objects.filter(item=item, members=request.user)

    if conversations.exists():
        return redirect('inbox')

    if request.method == 'POST':
        form = ConversationMessageForm(request.POST)

        if form.is_valid():
            conversation = Conversation.objects.create(item=item)
            conversation.members.add(request.user)
            conversation.members.add(item.author)

            conversation_message = form.save(commit=False)
            conversation_message.conversation = conversation
            conversation_message.created_by = request.user
            conversation_message.save()

            return redirect('inbox')
    else:
        form = ConversationMessageForm()

    return render(request, 'tasks_app_user/new.html', {
        'form': form
    })


@login_required
def inbox(request):
    conversations = Conversation.objects.filter(members__in=[request.user.id])
    return render(request, 'tasks_app_user/inbox.html', {
        'conversations': conversations,

    })


@login_required
def detail(request, pk):
    conversation = Conversation.objects.filter(members__in=[request.user.id]).get(pk=pk)
    interlocutor = conversation.members.exclude(id=request.user.id).first()

    if request.method == 'POST':
        form = ConversationMessageForm(request.POST)

        if form.is_valid():
            conversation_message = form.save(commit=False)
            conversation_message.conversation = conversation
            conversation_message.created_by = request.user
            conversation_message.save()

            conversation.save()

            return redirect('detail', pk=pk)
    else:
        form = ConversationMessageForm()

    return render(request, 'tasks_app_user/detail.html', {
        'conversation': conversation,
        'form': form,
        'interlocutor': interlocutor
    })
