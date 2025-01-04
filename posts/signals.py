from decimal import Decimal

from django.conf import settings


def add_rating(sender, instance, **kwargs):
    _update_rating(instance, is_adding=True)


def remove_rating(sender, instance, **kwargs):
    _update_rating(instance, is_adding=False)


def _update_rating(customer_rating, is_adding: bool = True):
    """
    update rating for a post after adding/removing a rating
    """

    # this is for adding more weight to older rates than new ones.
    # this way, when many people try to suddenly change the rate, it won't be possible.
    lamda = settings.LAMBDA

    previous_rating = customer_rating.post.average_rating * lamda
    rate_count = customer_rating.post.rate_count

    if is_adding:
        new_rating = (Decimal(previous_rating * rate_count) + customer_rating.rate) / Decimal(rate_count + 1)
        customer_rating.post.rate_count = rate_count + 1
    else:
        new_rating = (Decimal(previous_rating * rate_count) - customer_rating.rate) / Decimal(rate_count - 1)
        customer_rating.post.rate_count = rate_count - 1

    customer_rating.post.average_rating = new_rating
    customer_rating.post.save()
