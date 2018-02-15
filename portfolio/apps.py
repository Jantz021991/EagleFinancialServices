from django.apps import AppConfig


class PortfolioConfig(AppConfig):
    name = 'portfolio'

    # def ready(self):
    #     # Makes sure all signal handlers are connected
    #     from . import handlers # noqa
