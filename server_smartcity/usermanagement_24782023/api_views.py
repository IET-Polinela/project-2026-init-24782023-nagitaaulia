from rest_framework import generics
from .models import CustomUser
from .serializers import RegisterSerializer
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q

class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer