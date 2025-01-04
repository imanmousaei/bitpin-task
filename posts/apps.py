from django.apps import AppConfig

from django.db.models.signals import post_save, post_delete


class ExchangeConfig(AppConfig):
    name = 'posts'

    def ready(self):
        from .models import CustomerRating
        from .signals import add_rating, remove_rating

        post_save.connect(add_rating, sender=CustomerRating)
        post_delete.connect(remove_rating, sender=CustomerRating)
