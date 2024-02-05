from rest_framework import serializers
from django.core.validators import MinLengthValidator, RegexValidator
from rest_framework.validators import UniqueValidator
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'mobile_number', 'dob', 'profile_picture', 'is_active']


class RegisterSerializer(UserSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[
            MinLengthValidator(8),
            RegexValidator(
                regex=r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$',
                message='Password must contain at least eight characters, at least one letter, one number and one special character'
            ),
        ],
        error_messages={
            'blank': 'Password cannot be blank.',
            'required': 'Password is required.'
        }
    )
    username = serializers.CharField(
        validators=[
            UniqueValidator(queryset=User.objects.all()),
            RegexValidator(
                regex=r'^[a-zA-Z0-9_]+$',
                message='Username must contain only letters, numbers, and underscores.'
            ),
        ],
        error_messages={
            'unique': 'User with that username already exists.'
        }
    )
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())],
        error_messages={
            'unique': 'User with that email already exisits.'
        }
    )

    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + ['password']

    def create(self, validated_data):
        """
        Create a new user object based on the provided validated data.
        """
        user = User(
            email=validated_data['email'],
            username=validated_data['username'],
            mobile_number=validated_data.get('mobile_number'),
            dob=validated_data.get('dob'),
            profile_picture=validated_data.get('profile_picture')
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'), email=email, password=password)
            if user and user.is_active:
                data['user'] = user
                return data
            raise serializers.ValidationError('Incorrect email or password.')
        raise serializers.ValidationError('Please provide both email and password.')

    def create(self, validated_data):
        refresh = RefreshToken.for_user(validated_data['user'])
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
