from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token

User = get_user_model()


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["id", "username", "email", "password"]

    def create(self, validated_data):
        user = User(
            username=validated_data["username"],
            email=validated_data.get("email", ""),
            password=validated_data["password"],
        )
        Token.objects.create(user=user)
        return user


class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    password = serializers.CharField()


class UserSerializer(serializers.ModelSerializer):
    followers_count = serializers.IntegerField(source="followers.count", read_only=True)
    following_count = serializers.IntegerField(source="following.count", read_only=True)
    profile_picture_url = serializers.SerializerMethodField()

    class Meta:
        Model = User
        fields = [
            "id",
            "username",
            "email",
            "bio",
            "profile_picture_url",
            "followers_count",
            "following_count",
        ]

        def get_profile_picture_url(self, obj):
            request = self.context.get("request")
            if obj.profile_picture:
                return (
                    request.build_absolute_uri(obj.profile_picture.url)
                    if request
                    else obj.profilepicture.url
                )
            return None
