from decimal import Decimal

import pytest
from django.conf import settings
from django.contrib.auth.models import User
from django.forms import ValidationError
from django.test import TestCase, Client

from customers.models import Customer
from posts.models import Post, CustomerRating

pytestmark = pytest.mark.django_db


class TestEndpoints(TestCase):
    posts_endpoint = '/api/v1/posts/'
    rate_endpoint = posts_endpoint + 'rate'

    def setUp(self) -> None:
        # test create post
        title = 'Post Title'
        text = 'Post Text'
        post = Post.objects.create(title=title, text=text)
        assert post.title == title
        assert post.text == text
        assert Post.objects.filter(title=title, text=text).exists()

        # test create customer
        customer = Customer.objects.create(user=User.objects.create(username='imanmousaei', password='pass1234'))
        customer2 = Customer.objects.create(user=User.objects.create(username='imanmousaei2', password='pass1234'))
        customer3 = Customer.objects.create(user=User.objects.create(username='imanmousaei3', password='pass1234'))
        customer4 = Customer.objects.create(user=User.objects.create(username='imanmousaei4', password='pass1234'))
        assert Customer.objects.filter(user__username='imanmousaei').exists()

        # test valid rating
        customer_rating = CustomerRating.objects.create(customer=customer, rate=5, post=post)
        CustomerRating.objects.create(customer=customer2, rate=4, post=post)

        post.refresh_from_db()

        assert post.rate_count == 2
        assert post.average_rating == (Decimal(5) * settings.LAMBDA + Decimal(4)) / Decimal(2)

        # test invalid rating
        with pytest.raises(ValidationError):
            CustomerRating.objects.create(customer=customer3, rate=6, post=post)

        self.post = post
        self.customer = customer
        self.customer2 = customer2
        self.customer3 = customer3
        self.customer4 = customer4
        self.customer_rating = customer_rating
        self.client = Client()

    def test_get_posts(self):
        # test get all posts
        response = self.client.get(
            self.posts_endpoint,
            data={
                'customer_id': self.customer.id,
            }
        )
        assert response.status_code == 200
        first_post = response.json()[0]

        assert first_post['title'] == self.post.title
        assert Decimal(first_post['your_rating']) == self.customer_rating.rate
        assert first_post['rate_count'] == 2
        assert Decimal(first_post['average_rating']) == (Decimal(5) * settings.LAMBDA + Decimal(4)) / Decimal(2)

        # test get one post rating
        response = self.client.get(
            self.posts_endpoint,
            data={
                'customer_id': self.customer.id,
                'post_id': self.post.id
            }
        )

        post_info = response.json()
        assert Decimal(post_info['average_rating']) == self.post.average_rating

    def test_post_rate(self):
        # test valid rating
        response = self.client.post(
            f'{self.rate_endpoint}/{self.post.id}',
            {
                'customer_id': self.customer3.id,
                'rate': 5
            }
        )

        assert response.status_code in [201, 200]
        assert CustomerRating.objects.filter(customer=self.customer3, rate=5, post=self.post).exists()

        # test change rating
        response = self.client.post(
            f'{self.rate_endpoint}/{self.post.id}',
            {
                'customer_id': self.customer3.id,
                'rate': 4
            }
        )

        assert response.status_code in [201, 200]
        assert CustomerRating.objects.filter(customer=self.customer3, rate=4, post=self.post).exists()

        # test invalid rating
        response = self.client.post(
            f'{self.rate_endpoint}/{self.post.id}',
            {
                'customer_id': self.customer4.id,
                'rate': 6
            }
        )
        assert response.status_code == 400
