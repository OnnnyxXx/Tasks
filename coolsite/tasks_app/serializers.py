from rest_framework import serializers
from tasks_app_user.models import Profile, Comment


class ProfileSerializer(serializers.ModelSerializer):
    avg_rating = serializers.DecimalField(max_digits=3, decimal_places=2, read_only=True)

    class Meta:
        model = Profile
        fields = ('id', 'first_name', 'last_name', 'email', 'telegram_url', 'youtube_url', 'vk_url', 'profile_picture',
                  'city', 'user', 'avg_rating')

