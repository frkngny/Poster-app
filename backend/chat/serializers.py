from .models import Conversation, Message
from account.serializers import UserSerializer
from rest_framework import serializers

class ConversationSerializer(serializers.ModelSerializer):
    users = UserSerializer(read_only=True, many=True)
    class Meta:
        model = Conversation
        fields = ['id', 'users', 'updated_at_formatted']

class MessageSerializer(serializers.ModelSerializer):
    sender = UserSerializer(read_only=True)
    receiver = UserSerializer(read_only=True)
    class Meta:
        model = Message
        fields = ['id', 'sender', 'receiver', 'body', 'created_at_formatted']

class ChatDetailSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(read_only=True, many=True)
    
    class Meta:
        model = Conversation
        fields = ['id', 'users', 'updated_at_formatted', 'messages']
    