from django.shortcuts import get_object_or_404
from .serializers import RegistrationSerializer, LoginSerializer, UserSerializer
from django.contrib.auth import authenticate, get_user_model
from rest_framework.views import APIView
from rest_framework import status, permissions, generics
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import CustomUser


class RegisterView(APIView):
    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileView(APIView):
    authentication_classes = [
        TokenAuthentication
    ]  # only users with a valid token can access
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user  # the logged-in user automatically set by token auth
        data = {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "bio": user.bio,
            "profile_picture": (
                request.build_absolute_uri(user.profile_picture.url)
                if user.profile_picture
                else None
            ),
            "followers_count": user.followers.count(),
            "following_count": user.following_count(),
        }  # build absolute uri turns the picture url into a full url
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


class FollowUserView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = CustomUser.objects.all()

    def post(self, request, user_id):
        try:
            user_to_follow = CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            return Response(
                {"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND
            )

        request.user.following.add(user_to_follow)
        return Response({"detail": "Followed successfully"})


class UnfollowUserView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = CustomUser.objects.all()

    def post(self, request, user_id):
        try:
            user_to_unfollow = CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            return Response(
                {"detail": "User not found"}, status=status.HTTP_404_NOT_FOUND
            )

        request.user.following.remove(user_to_unfollow)
        return Response({"detail": "Unfollowed successfully"})


class UserFollowingList(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        qs = request.user.following.all()
        serializer = UserSerializer(qs, many=True, context={"request": request})
        return Response(serializer.data)
