from django.urls import path
from .views import PostList, PostDetail, PostCreate, ProfilePostList, PostLike, PostComment, TrendTags

urlpatterns = [
    path('', PostList.as_view(), name='post-list'),
    path('trend_tags', TrendTags.as_view(), name='trend-tags'),
    path('create', PostCreate.as_view(), name='post-create'),
    path('profile/<uuid:id>', ProfilePostList.as_view(), name='post-list-profile'),
    path('<uuid:pk>/like', PostLike.as_view(), name='post-like'),
    path('<uuid:pk>/comment', PostComment.as_view(), name='post-comment'),
    path('<uuid:pk>', PostDetail.as_view(), name='post-detail'),
]