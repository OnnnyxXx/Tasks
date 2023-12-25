from django.urls import path

from . import views
from .views import *


urlpatterns = [
    path('', views.profile, name='profile'),
    path('user_home/', views.User_View, name='user_home'),
    path('profile_user/<int:id>/', views.user_profile, name='user_profile'),
    path('profile_user/<int:id>/add_comment/', views.AddCommentView, name='add_comment'),
    path('comment/update/<int:pk>/', CommentUpdateView.as_view(), name='update_comment'),
    path('comment/delete/<int:pk>/', CommentDeleteView.as_view(), name='delete_comment'),
]