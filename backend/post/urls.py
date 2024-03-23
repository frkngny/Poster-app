from django.urls import path
from .views import PostList, PostCreate, ProfilePostList, PostLike

urlpatterns = [
    path('', PostList.as_view(), name='post-list'),
    path('create', PostCreate.as_view(), name='post-create'),
    path('like', PostLike.as_view(), name='post-like'),
    path('profile/<uuid:id>', ProfilePostList.as_view(), name='post-list-profile'),
]