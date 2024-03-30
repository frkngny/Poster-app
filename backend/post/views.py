from django.shortcuts import render
from django.http import JsonResponse
from .serializers import PostSerializer, PostDetailSerializer, CommentSerializer
from .models import Post, Like, Comment
from rest_framework.decorators import api_view
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView
from .forms import PostForm
from django.db.models import Q

class PostList(ListAPIView):
    serializer_class = PostSerializer
    def get(self, request, *args, **kwargs):
        posts = Post.objects.all()
        if request.GET.get('in_friends'):
            user_friends = request.user.friends.all()
            posts = Post.objects.filter(Q(created_by_id=request.user.id) | Q(created_by_id__in=user_friends))
        serializer = self.serializer_class(posts, many=True)
        return JsonResponse(serializer.data, safe=False)

class PostDetail(RetrieveAPIView):
    serializer_class = PostDetailSerializer
    def get(self, request, *args, **kwargs):
        if kwargs.get('pk'):
            post = Post.objects.get(pk=kwargs.get('pk'))
            return JsonResponse(self.serializer_class(post).data)
        return JsonResponse({'message': 'Please provide a correct id.'})

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

class PostLike(CreateAPIView):
    def post(self, request, *args, **kwargs):
        user = request.user
        
        post_id = kwargs.get('pk')
        post = Post.objects.get(id=post_id)
        
        if user not in post.liked.all():
            like = Like.objects.create(user=user, post=post)
        else:
            like = Like.objects.get(user=user, post=post)
            like.delete()
        
        return JsonResponse({'post': PostDetailSerializer(like.post).data})

class PostComment(CreateAPIView, ListAPIView):
    def get(self, request, *args, **kwargs):
        post_id = kwargs.get('pk')
        post = Post.objects.get(id=post_id)
        comments = Comment.objects.filter(post=post)
        return JsonResponse(CommentSerializer(comments, many=True).data, safe=False)
    
    def post(self, request, *args, **kwargs):
        user = request.user
        
        post_id = kwargs.get('pk')
        post = Post.objects.get(id=post_id)
        
        if request.data.get('body'):
            comment = Comment.objects.create(user=user, post=post, body=request.data.get('body'))
            return JsonResponse({'post': PostSerializer(comment.post).data, 'comment': CommentSerializer(comment).data})
        return JsonResponse({'error': 'Cannot create comment'})