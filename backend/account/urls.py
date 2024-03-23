from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import api
from .views import GetUserProfile, FriendshipRequest, Friends

urlpatterns = [
    path('login', TokenObtainPairView.as_view(), name='token_obtain'),
    path('refresh-token', TokenRefreshView.as_view(), name='token_refresh'),
    path('signup', api.signup, name='signup'),
    path('me', api.me, name='me'),
    path('user/<uuid:id>', GetUserProfile.as_view(), name='user'),
    path('user/<uuid:id>/friends', Friends.as_view(), name='friends'),
    path('user/<uuid:id>/friends/request', FriendshipRequest.as_view(), name='friend-request'),
]