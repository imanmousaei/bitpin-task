from decimal import Decimal

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.forms import ValidationError

from customers.models import Customer


class Post(models.Model):
    title = models.CharField(max_length=63, verbose_name=_('Article Title'))
    text = models.TextField(max_length=1023, verbose_name=_('Article text'))

    rate_count = models.PositiveBigIntegerField(default=0, verbose_name=_('Number of ratings for this post'))
    average_rating = models.DecimalField(max_digits=6, decimal_places=3, default=Decimal(0.0),
                                         verbose_name=_('Average Rating for this post'))

    def __str__(self):
        return self.title


class CustomerRating(models.Model):
    """
    Each row is a single rating of a user for a post
    """

    RATE_CHOICES = (
        (0, _('Shit')),
        (1, _('Very Poor')),
        (2, _('Poor')),
        (3, _('Neutral')),
        (4, _('Good')),
        (5, _('Excellent')),
    )
    RATE_VALUES = [choice[0] for choice in RATE_CHOICES]

    rate = models.PositiveSmallIntegerField(choices=RATE_CHOICES)
    timestamp = models.DateTimeField(auto_now_add=True)

    customer = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if self.rate not in self.RATE_VALUES:
            raise ValidationError('Rate must be between 0 to 5')
        super().save(*args, **kwargs)

    class Meta:
        unique_together = (('customer', 'post'),)

    def __str__(self):
        return f'rating {self.rate} for post id {self.post.id} from user {self.customer.username}'
