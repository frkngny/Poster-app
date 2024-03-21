from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.generics import ListAPIView
from .serializers import UserSerializer
from .models import User

class GetUserProfile(ListAPIView):
    serializer_class = UserSerializer
    def get(self, request, id):
        user = User.objects.get(id=id)
        serializer = self.serializer_class(user)
        return JsonResponse(serializer.data)
