from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.generics import ListAPIView
from account.models import User
from account.serializers import UserSerializer
from post.models import Post
from post.serializers import PostSerializer


class Search(ListAPIView):
    def get(self, request, *args, **kwargs):
        query = request.query_params.get('query')
        
        users = User.objects.filter(name__icontains=query)
        user_serializer = UserSerializer(users, many=True)
        
        posts = Post.objects.filter(body__icontains=query)
        posts_serializer = PostSerializer(posts, many=True)
        
        return JsonResponse({'users': user_serializer.data, 'posts': posts_serializer.data}, safe=False)