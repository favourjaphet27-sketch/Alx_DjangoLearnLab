from django.shortcuts import get_object_or_404
from .serializers import RegistrationSerializer, LoginSerializer, UserSerializer
from django.contrib.auth import authenticate, get_user_model
from rest_framework.views import APIView
from rest_framework import status, permissions
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

# Create your views here.
User = get_user_model()


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


class FollowUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id):
        if request.user.id == user_id:
            return Response(
                {"detail": "You can't follow yourself."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        target = get_object_or_404(User, id=user_id)
        request.user.following.add(target)
        request.user.save()
        data = {
            "following_count": request.user.following.count(),
            "followers_count_target": target.followers.count(),
        }
        return Response(data, status=status.HTTP_200_OK)


class UnfollowUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id):
        if request.user.id == user_id:
            return Response(
                {"detail": "You can't unfollow yourself."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        target = get_object_or_404(User, id=user_id)
        request.user.following.remove(target)
        request.user.save()
        data = {
            "following_count": request.user.following.count(),
            "followers_count_target": target.followers.count(),
        }
        return Response(data, status=status.HTTP_200_OK)


class UserFollowingList(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        qs = request.user.following.all()
        serializer = UserSerializer(qs, many=True, context={"request": request})
        return Response(serializer.data)
