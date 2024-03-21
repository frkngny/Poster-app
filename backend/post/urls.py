from django.urls import path
from .views import PostList, PostCreate, ProfilePostList

urlpatterns = [
    path('', PostList.as_view(), name='post-list'),
    path('create', PostCreate.as_view(), name='post-create'),
    path('profile/<uuid:id>', ProfilePostList.as_view(), name='post-list-profile'),
]