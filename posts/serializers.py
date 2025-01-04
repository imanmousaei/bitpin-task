from rest_framework import serializers

from posts.models import *


class PostSerializer(serializers.ModelSerializer):
    your_rating = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = '__all__'

    def get_your_rating(self, obj):
        customer_id = self.context['customer_id']

        # check if the user has rated this post
        try:
            customer_rating = CustomerRating.objects.get(customer_id=customer_id, post=obj)
            return customer_rating.rate
        except CustomerRating.DoesNotExist:
            return None


class CustomerRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerRating
        fields = '__all__'
