from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        ordering = ("name",)

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=255)
    contents = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    published_date = models.DateTimeField(auto_now_add=True)

    # Tags relationship
    tags = models.ManyToManyField(Tag, blank=True, related_name="posts")

    def get_absolute_url(self):
        return reverse("blog:post-detail", kwargs={"pk": self.pk})

    def __str__(self):
        return self.title


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    image = models.ImageField(upload_to="profile_images/", blank=True, null=True)

    def __str__(self):
        return f"Profile of {self.user.username}"

    def get_absolute_url(self):
        return reverse("profile")


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
