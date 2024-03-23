from django.contrib import admin
from .models import Post, PostAttachment, Like

admin.site.register(Post)
admin.site.register(PostAttachment)
admin.site.register(Like)