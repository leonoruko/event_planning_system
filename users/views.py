from django.shortcuts import render
from django.contrib.auth import get_user_model
from rest_framework import generics,permissions
from .serializers import UserSerializer
from allauth.account.views import ConfirmEmailView
from django.http import JsonResponse
# Create your views here.

User=get_user_model()

class ProfileDetailView(generics.RetrieveUpdateAPIView):
    queryset=User.objects.all()
    serializer_class=UserSerializer
    permission_classes=[permissions.IsAuthenticated]


    def get_object(self):
        return self.request.user

class CustomConfirmEmailView(ConfirmEmailView):
    def get(self,*args,**kwargs):
        confirmation=self.get_object()
        confirmation.confirm(self.request)
        return JsonResponse({'detail':'Email Confirmed successfully'},status=200)
