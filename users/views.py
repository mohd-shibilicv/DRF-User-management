from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from django.contrib.auth import login

from users.models import User
from users.serializers import LoginSerializer
from users.serializers import RegisterSerializer


class HelloWorld(APIView):
    def get(self, request):
        return Response({'message': 'Mohammed Shibili cv'})


class UserListView(APIView):
    def get(self, request):
        users = User.objects.all()
        user_list = []
        for user in users:
            user_list.append({
                'id': user.id,
                'email': user.email,
                'username': user.username,
                'mobile_number': user.mobile_number if user.mobile_number else None,
                'dob': user.dob if user.dob else None,
                'profile_picture': user.profile_picture if user.profile_picture else None,
                'is_active': user.is_active,
                'is_verified': user.is_verified
            })
        return Response(user_list)


class ProtectedView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"detail": "This is a protected view."}, status=200)


class RegisterView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer

    def perform_create(self, serializer):
        serializer.save()

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)

        if response.status_code == status.HTTP_201_CREATED:
            # Add a custom success message to the response
            response.data['message'] = 'User registered successfully. Welcome!'

        return response


class LoginView(generics.GenericAPIView):
    serializer_class =  LoginSerializer

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            login(request, user)
            return Response(serializer.create(serializer.validated_data), status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def finalize_response(self, request, response, *args, **kwargs):
        if response.status_code == 200:
            access_token = response.data['access']
            refresh_token = response.data['refresh']
            response.set_cookie('access_token', access_token, httponly=True)
            response.set_cookie('refresh_token', refresh_token, httponly=True)
        return super().finalize_response(request, response, *args, **kwargs)
