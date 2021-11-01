from django.apps import AppConfig


class ServerConfig(AppConfig):
    name = 'server'
    def ready(self):
        import server.signals


class MyappConfig(AppConfig):
    name = 'backend'
    def ready(self):
        from . import updater
        updater.start()

    