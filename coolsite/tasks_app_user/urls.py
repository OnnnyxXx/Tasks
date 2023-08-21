from django.urls import path, include
from . import views
from .views import *


urlpatterns = [
    path('', views.tasks_home, name='tasks_home'),
    path('/create/', views.create, name='create'),
    path('/<int:pk>', views.TasksDetailView.as_view(), name='details_tasks'),
    path('register/', views.RegisterUser.as_view(), name='register'),
    path('login/', views.LoginUser.as_view(), name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('/<int:pk>/u', views.TasksUpdateView.as_view(), name='update_tasks'),
    path('/<int:pk>/d', views.TasksDeleteView.as_view(), name='delete_tasks'),
]