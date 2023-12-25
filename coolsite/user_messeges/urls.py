from django.urls import path

from . import views
from .views import *


urlpatterns = [
    path('messages/<int:pk>/', views.detail, name='detail'),
    path('message/', views.inbox, name='inbox'),
    path('new/<int:item_pk>/', views.new_conversation, name='new'),

]