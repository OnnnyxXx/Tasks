from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter

# from tasks_app.views import TopUsersViewSet
#
# router = DefaultRouter()
# router.register(r'home', TopUsersViewSet, basename='home')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('tasks_app.urls')),
    # path('', include(router.urls)),
    path('tasks/', include('tasks_app_user.urls')),


]+ static(settings.STATIC_URL, document_root=settings.STATIC_URL)
if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


