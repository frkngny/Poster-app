from django.shortcuts import render
from django.http import JsonResponse
from .serializers import PostSerializer
from .models import Post
from rest_framework.decorators import api_view
from rest_framework.generics import ListAPIView, CreateAPIView
from .forms import PostForm

class PostList(ListAPIView):
    serializer_class = PostSerializer
    def get(self, request):
        posts = Post.objects.all()
        serializer = self.serializer_class(posts, many=True)
        return JsonResponse(serializer.data, safe=False)

class ProfilePostList(ListAPIView):
    serializer_class = PostSerializer
    def get(self, request, id):
        posts = Post.objects.filter(created_by_id=id)
        serializer = self.serializer_class(posts, many=True)
        return JsonResponse(serializer.data, safe=False)

class PostCreate(CreateAPIView):
    serializer_class = PostSerializer
    def post(self, request):
        form = PostForm(request.data)
        if form.is_valid():
            post = form.save(commit=False)
            post.created_by = request.user
            post.save()
            return JsonResponse(self.serializer_class(post).data, safe=False)
        return JsonResponse({'error': 'error'})