from django.shortcuts import render
from .serializers import RegistrationSerializer, LoginSerializer
from django.contrib.auth import authenticate, get_user_model
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

# Create your views here.


class RegisterView(APIView):
    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, _ = Token.objects.get_or_create(user=user)
            return Response({"token": token.key}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class ProfileView(APIView):
    authentication_classes = [TokenAuthentication] # only users with a valid token can access
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user # the logged-in user automatically set by token auth
        data = {
            'id': user.id, 'username': user.username, 'email':user.email, 'bio':user.bio, 'profile_picture': request.build_absolute_uri(user.profile_picture.url) if user.profile_picture else None, 'followers_count': user.followers.count(), 'following_count': user.following_count(),
        } # build absolute uri turns the picture url into a full url
        return Response(data, status=status.HTTP_200_OK)



class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(
            username=serializer.validated_data["username"],
            password=serializer.validated_data["password"],
        )
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({"token": token.key}, status=status.HTTP_200_OK)
        return Response(
            {"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST
        )
