from .models import Post, Comment
from account.serializers import UserSerializer
from rest_framework import serializers

class PostSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    class Meta:
        model = Post
        fields = ['id', 'body', 'created_by', 'created_at_formatted', 'likes_count', 'comments_count']
        
class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Comment
        fields = ['id', 'body', 'user', 'post', 'created_at_formatted']
        
class PostDetailSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    liked = UserSerializer(read_only=True, many=True)
    post_comments = CommentSerializer(read_only=True, many=True)
    class Meta:
        model = Post
        fields = ['id', 'body', 'created_by', 'created_at_formatted', 'likes_count', 'liked', 'comments_count', 'post_comments']