from django.apps import AppConfig


class BulletinboardConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'BulletinBoard'

    # set signals (INSTALLED_APPS => 'BulletinBoard.apps.BulletinboardConfig')
    def ready(self):
        import BulletinBoard.signals
