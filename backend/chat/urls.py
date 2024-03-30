from django.urls import path
from .views import Conversations, ChatDetail

urlpatterns = [
    path('', Conversations.as_view(), name='conversations'),
    path('<uuid:pk>', ChatDetail.as_view(), name='chat_detail'),
    path('<uuid:pk>/send', ChatDetail.as_view(), name='send_chat_message'),
]