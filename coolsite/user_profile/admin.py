from django.utils.safestring import mark_safe

from .models import Profile, Comment

from django.contrib import admin


# admin.site.register(Profile)
# admin.site.register(Comment)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'get_html_photo', 'user', 'first_name', 'last_name', 'email', 'city')
    list_display_links = ('id', 'user', 'first_name', 'last_name')
    list_filter = ('city', 'user')
    search_fields = ("first_name",)
    fields = (
        'user', 'first_name', 'last_name', 'email', 'telegram_url', 'youtube_url', 'vk_url', 'profile_picture',
        'get_html_photo',
        'city')
    readonly_fields = ('get_html_photo',)

    def get_html_photo(self, object):
        if object.profile_picture:
            return mark_safe(f"<img src='{object.profile_picture.url}' width=50>")

    get_html_photo.short_description = 'Миниатюра'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'author', 'profile', 'content', 'stars', 'created_at')
    list_filter = ('author', 'profile', 'stars')
    list_display_links = ('id', 'author', 'profile', 'stars')
    search_fields = ("profile",)  # Need Fix
    fields = ('author', 'profile', 'content', 'stars', 'created_at')
    readonly_fields = ('created_at',)
