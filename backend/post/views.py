from django.shortcuts import render
from django.http import JsonResponse
from .serializers import PostSerializer, PostDetailSerializer, CommentSerializer
from .models import Post, Like, Comment
from rest_framework.decorators import api_view
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework import status
from .forms import PostForm
from django.db.models import Q
from datetime import datetime, timedelta, timezone
import sys
sys.path.append("..")
from utils import generate_trends


class PostList(ListAPIView):
    serializer_class = PostSerializer
    def get(self, request, *args, **kwargs):
        posts = Post.objects.all()
        if request.GET.get('in_friends', 'false'):
            user_friends = request.user.friends.all()
            posts = Post.objects.filter(Q(created_by_id=request.user.id) | Q(created_by_id__in=user_friends))
        else:
            posts = Post.objects.all()
            
        if 'trend' in request.GET:
            tag = request.GET.get('trend')
            posts = Post.objects.filter(body__icontains='#'+tag)
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


trend_range_n_hours = 30
trends_upto = 5

class TrendTags(ListAPIView):
    permission_classes = []
    def get(self, request):
        trends = generate_trends.generate(date_range_hours=trend_range_n_hours)[:trends_upto]
        trends_tags = [{'tag': x, 'count': y} for x,y in trends]
        return JsonResponse(trends_tags, safe=False)

class TrendPosts(ListAPIView):
    permission_classes = []
    serializer_class = PostSerializer
    def get_queryset(self):
        trends = generate_trends.generate(date_range_hours=trend_range_n_hours)[:trends_upto]
        trends_tags = [x for x,y in trends]
        
        from_date = generate_trends.get_date_range(trend_range_n_hours)
        
        body_query = Q(body__icontains=trends_tags[0])
        for tag in trends_tags[1:]:
            body_query = body_query | Q(body__icontains=tag)
        
        trend_posts = Post.objects.filter(created_at__gte=from_date).filter(body_query)
        return trend_posts