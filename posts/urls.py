from django.urls import path

from .views import PostsView,RatingView

app_name = 'posts'


urlpatterns = [
    path('', view=PostsView.as_view(), name='posts_list'),
    path('rate/<int:post_id>', view=RatingView.as_view(), name='rate'),

]
