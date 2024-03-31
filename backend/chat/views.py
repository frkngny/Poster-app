from django.http import JsonResponse
from .serializers import ConversationSerializer, MessageSerializer, ChatDetailSerializer
from .models import Conversation, Message
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView, GenericAPIView
from rest_framework import status

from account.models import User


class Conversations(ListAPIView):
    serializer_class = ConversationSerializer
    def get(self, request, *args, **kwargs):
        conversations = Conversation.objects.filter(users__in=[request.user])
        serializer = self.serializer_class(conversations, many=True)
        return JsonResponse(serializer.data, safe=False)

class ConversationView(ListAPIView):
    def get(self, request, *args, **kwargs):
        user = User.objects.get(pk=kwargs.get('user_pk'))
        conversation, created = Conversation.objects.filter(users__in=[request.user]).filter(users__in=[user]).get_or_create()
        if created:
            conversation.users.add(request.user, user)
        return JsonResponse({'conversation': ConversationSerializer(conversation).data})

class ChatDetail(ListAPIView, CreateAPIView):
    serializer_class = ChatDetailSerializer
    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        chatDetail = Conversation.objects.filter(users__in=[request.user]).get(pk=pk)
        serializer = ChatDetailSerializer(chatDetail)
        return JsonResponse(serializer.data, safe=False)
    
    def post(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        conversation = Conversation.objects.filter(users__in=[request.user]).get(pk=pk)
        
        receiver = None
        for user in conversation.users.all():
            if user != request.user:
                receiver = user 
        if request.data.get('body') and len(request.data.get('body')) > 0:
            message = Message.objects.create(conversation=conversation, body=request.data.get('body'), sender=request.user, receiver=receiver)
            serializer = MessageSerializer(message)
            return JsonResponse(serializer.data)
        return JsonResponse({'error': 'Please type something.'}, status=status.HTTP_400_BAD_REQUEST)
