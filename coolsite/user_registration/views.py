from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import CreateView
from rest_framework import generics
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate, login, logout, get_user_model

from user_registration.forms import RegisterUserForm, LoginUserForm


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'register.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return dict(list(context.items()))

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


# class RegisterUserView(CreateAPIView):
#     serializer_class = RegisterUserSerializer
#
#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#
#         user = self.perform_create(serializer)
#
#         refresh = RefreshToken.for_user(user)
#         token_data = {
#             'refresh': str(refresh),
#             'access': str(refresh.access_token),
#         }
#
#         headers = self.get_success_headers(serializer.data)
#         return Response(token_data, status=status.HTTP_201_CREATED, headers=headers)
#
#     def perform_create(self, serializer):
#         return serializer.save()


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return dict(list(context.items()))

    def get_success_url(self):
        return reverse_lazy('home')


# class LoginUserView(APIView):
#     def get(self, request, *args, **kwargs):
#         return Response({"detail": "GET request is not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
#
#     def post(self, request, *args, **kwargs):
#         serializer = LoginUserSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         user = serializer.validated_data['user']
#
#         refresh = RefreshToken.for_user(user)
#         token_data = {
#             'refresh': str(refresh),
#             'access': str(refresh.access_token),
#         }
#
#         return redirect('tasks_home')
#

def logout_user(request):
    logout(request)
    return redirect('login')
