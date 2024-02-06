from django.conf import settings
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from django.contrib.auth import login

from users.models import User
from users.serializers import RegisterSerializer, LoginSerializer, UserSerializer


class HelloWorld(APIView):
    def get(self, request):
        return Response({'message': 'Mohammed Shibili cv'})


class UserListView(APIView):
    def get(self, request):
        users = User.objects.filter(is_active=True)
        serializer = UserSerializer(users, many=True, context={'request': request})
        return Response(serializer.data)


class UserAccountView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user


class ProtectedView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"detail": "This is a protected view."}, status=200)


class RegisterView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    parser_classes = (MultiPartParser, FormParser)
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


@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def deactivate_user(request):
    user = request.user
    user.is_active = False
    user.save()
    return Response({'status': 'User deactivated'}, status=status.HTTP_200_OK)


class UserProfileUpdateView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user
