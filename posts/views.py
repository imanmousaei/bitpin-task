from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from posts.cache_service import CacheService
from posts.models import Post, CustomerRating
from posts.serializers import PostSerializer


class PostsView(APIView):
    def get(self, request):
        # we don't have auth here because you said to implement in the easiest form
        customer_id = request.GET.get('customer_id')
        post_id = request.GET.get('post_id')

        if post_id:
            cache_key = f'post_{post_id}'
            rating = CacheService.get_decimal(cache_key)
            if rating is None:
                rating = Post.objects.filter(id=post_id).values_list('average_rating', flat=True).first()
                CacheService.set_decimal(cache_key, rating)
            return Response([{'id': post_id, 'average_rating': rating}], status=status.HTTP_200_OK)
        else:
            posts_list = Post.objects.all()
            serializer = PostSerializer(posts_list, many=True, context={'customer_id': customer_id})
            return Response(serializer.data, status=status.HTTP_200_OK)


class RatingView(APIView):
    def post(self, request, post_id):
        try:
            # we don't have auth here because you said to implement in the easiest form
            customer_id = request.POST.get('customer_id')
            rate = int(request.POST.get('rate'))

            _, created = CustomerRating.objects.update_or_create(
                customer_id=customer_id, post_id=post_id, defaults={'rate': rate}
            )

            if created:
                return Response('Created successfully', status=status.HTTP_201_CREATED)
            else:
                return Response('Updated successfully', status=status.HTTP_200_OK)

        except Exception as exc:
            return Response(f'Error: {exc}', status=status.HTTP_400_BAD_REQUEST)
