from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from . import views
from .views import *


urlpatterns = [
    path('', views.tasks_home, name='tasks_home'),
    path('create/', views.create, name='create'),
    path('category/', views.category, name='category'),
    path('<int:pk>', views.TasksDetailView.as_view(), name='details_tasks'),
    path('register/', views.RegisterUser.as_view(), name='register'),
    path('login/', views.LoginUser.as_view(), name='login'),
    # path('api/register/', views.RegisterUserView.as_view(), name='register-api'),
    # path('api/tasks-auth/', include('rest_framework.urls')),
    # path('api/v1/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('api/v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('api/v1/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('logout/', views.logout_user, name='logout'),
    path('<int:pk>/update', views.TasksUpdateView.as_view(), name='update_tasks'),
    path('<int:pk>/delete', views.TasksDeleteView.as_view(), name='delete_tasks'),
    path('profile/', views.profile, name='profile'),
    # path('user_home/', views.User_View, name='user_home'),
    # path('profile/', views.profile, name='profile'),
    path('user_home/', views.User_View, name='user_home'),
    path('profile_user/<str:username>/', views.user_profile, name='user_profile'),
    path('profile_user/<str:username>/add_comment/', views.AddCommentView, name='add_comment'),
    path('comment/update/<int:pk>/', CommentUpdateView.as_view(), name='update_comment'),
    path('comment/delete/<int:pk>/', CommentDeleteView.as_view(), name='delete_comment'),
    path('messages/<int:pk>/', views.detail, name='detail'),
    path('message/', views.inbox, name='inbox'),
    path('new/<int:item_pk>/', views.new_conversation, name='new'),
]
