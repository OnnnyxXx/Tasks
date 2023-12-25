from django.urls import path, include

from . import views
from .views import *


urlpatterns = [
    path('', views.tasks_home, name='tasks_home'),
    path('create/', views.create, name='create'),
    path('category/', views.category, name='category'),
    path('<int:pk>', views.TasksDetailView.as_view(), name='details_tasks'),

    path('<int:pk>/update', views.TasksUpdateView.as_view(), name='update_tasks'),
    path('<int:pk>/delete', views.TasksDeleteView.as_view(), name='delete_tasks'),

]
