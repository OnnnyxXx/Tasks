# from rest_framework import serializers
# from django.contrib.auth.password_validation import validate_password
# from django.contrib.auth.models import User
# from .models import Profile, Comment
#
# """Регистрация"""
#
#
# class RegisterUserSerializer(serializers.ModelSerializer):
#     password2 = serializers.CharField(write_only=True)
#
#     class Meta:
#         model = User
#         fields = ['username', 'email', 'password', 'password2']
#
#     def validate_password(self, value):
#         validate_password(value)
#         return value
#
#     def create(self, validated_data):
#         user = User.objects.create(
#             username=validated_data['username'],
#             email=validated_data['email']
#         )
#         user.set_password(validated_data['password'])
#         user.save()
#         return user
#
#
# """Авторизация"""
#
#
# class LoginUserSerializer(serializers.Serializer):
#     username = serializers.CharField()
#     password = serializers.CharField(write_only=True)
#
#
# class CommentSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Comment
#         fields = ('author', 'profile', 'content', 'stars', 'created_at')
#
#
# class ProfileSerializer(serializers.ModelSerializer):
#     comments = CommentSerializer(many=True, read_only=True)
#
#     class Meta:
#         model = Profile
#         fields = (
#         'user', 'first_name', 'last_name', 'email', 'telegram_url', 'youtube_url', 'vk_url', 'profile_picture', 'city',
#         'comments', 'rating')
