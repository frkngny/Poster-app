from django.shortcuts import render
from django.http import JsonResponse
from rest_framework import status
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveUpdateAPIView
from .serializers import UserSerializer, FriendshipSerializer
from .models import User, Friendship
from django.db.models import Q

class GetUserProfile(ListAPIView):
    serializer_class = UserSerializer
    def get(self, request, id):
        user = User.objects.get(id=id)
        serializer = self.serializer_class(user)
        return JsonResponse(serializer.data)

class FriendshipRequest(CreateAPIView, ListAPIView, RetrieveUpdateAPIView):
    def get(self, request, *args, **kwargs):
        id = kwargs.get('id')
        user = User.objects.get(pk=id)
        received = Friendship.objects.filter(receiver=user, status=Friendship.SENT)
        sent = Friendship.objects.filter(sender=user, status=Friendship.SENT)
        return JsonResponse({'received_requests': FriendshipSerializer(received, many=True).data, 'sent_requests': FriendshipSerializer(sent, many=True).data})
    
    def post(self, request, *args, **kwargs):
        receiver_id = request.data.get('receiver')
        receiver_ = User.objects.get(pk=receiver_id)
        
        friendship_requests = Friendship.objects.filter((Q(sender=request.user) & Q(receiver=receiver_)) | (Q(sender=receiver_) & Q(receiver=request.user))).filter(Q(status=Friendship.SENT) | Q(status=Friendship.ACCEPTED))
        if not friendship_requests.exists():
            friend_request = Friendship.objects.create(sender=request.user, receiver=receiver_)
            return JsonResponse({'message': 'Request is sent'})
        return JsonResponse({'message': 'You are either friends or there is a pending request.'}, status=status.HTTP_406_NOT_ACCEPTABLE)
    
    def put(self, request, *args, **kwargs):
        status = request.data.get('status')
        sender_id = request.data.get('sender_id')
        sender_ = User.objects.get(pk=sender_id)
        
        friend_request = Friendship.objects.get(sender=sender_, receiver=request.user, status=Friendship.SENT)
        if friend_request:
            friend_request.status = status
            friend_request.save()
            return JsonResponse({'message': f'friend request is {status}'})
        return JsonResponse({'message': 'no request found'})

class Friends(ListAPIView):
    def get(self, request, id):
        user = User.objects.get(id=id)
        friends = user.friends.all()
        return JsonResponse({'user': UserSerializer(user).data, 'friends': UserSerializer(friends, many=True).data}, safe=False)