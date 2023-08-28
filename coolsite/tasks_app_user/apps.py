from django.apps import AppConfig


class TasksAppUserConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tasks_app_user'

    def ready(self):
        import tasks_app_user.signals