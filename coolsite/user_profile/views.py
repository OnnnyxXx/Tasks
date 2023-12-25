from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Avg
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import DeleteView, UpdateView

from user_profile.forms import CommentForm, ProfileForm
from user_profile.models import Comment


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
    return render(request, 'profile.html', context)


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

    return render(request, 'home_user.html', context)


def user_profile(request, id):
    user = get_object_or_404(User, id=id)
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

    return render(request, 'user_profile.html', context)


def AddCommentView(request, id):
    user = get_object_or_404(User, id=id)

    if request.method == 'POST':
        form = CommentForm(request.POST)

        if form.is_valid():
            author = request.user
            profile = user.profile  # Get the profile of the user being reviewed
            content = form.cleaned_data['content']
            stars = form.cleaned_data['stars']
            Comment.objects.create(author=author, profile=profile, content=content, stars=stars)
            return redirect('user_profile', user.id)

    else:
        form = CommentForm()

    return render(request, 'user_reviews.html', {'form': form, 'user': user})


# UpdateComment
@method_decorator(login_required, name='dispatch')
class CommentUpdateView(UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'user_reviews.html'
    success_url = reverse_lazy('user_profile', id=User.id)

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
        return reverse_lazy('user_profile', kwargs={'id': user.id})


# DeleteComment

@method_decorator(login_required, name='dispatch')
class CommentDeleteView(DeleteView):
    model = Comment
    success_url = reverse_lazy('user_profile')
    template_name = 'delete_comment.html'

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
        return reverse_lazy('user_profile',  kwargs={'id': user.id})