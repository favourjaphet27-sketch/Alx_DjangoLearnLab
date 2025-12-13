from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from .models import Post

User = get_user_model()


class PostCommentAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="u1", password="pass")
        self.token = self.client.post(
            reverse("register"), {"username": "u1", "password": "pass"}
        ).data.get("token")
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token}")

    def test_create_post(self):
        response = self.client.post(
            "/api/posts/", {"title": "T", "content": "C"}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(Post.objects.first().author, self.user)

    def test_comment_permission(self):
        post = Post.objects.create(author=self.user, title="a", content="b")
        response = self.client.post(
            "/api/comments/", {"post": post.id, "content": "x"}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # attempt delete as different user
        other = User.objects.create_user(username="other", password="p2")
        # authenticate as other
        self.client.force_authenticate(user=other)
        del_resp = self.client.delete(f'/api/comments/{response.data["id"]}/')
        self.assertEqual(del_resp.status_code, status.HTTP_403_FORBIDDEN)


class FeedTests(APITestCase):
    def setUp(self):
        self.u1 = User.objects.create_user(username="u1", password="p")
        self.u2 = User.objects.create_user(username="u2", password="p2")
        Post.objects.create(author=self.u2, title="hi", content="x")
        # login as u1 and follow u2
        resp = self.client.post(
            "/auth/login/", {"username": "u1", "password": "p"}, format="json"
        )
        token = resp.data.get("token")
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {token}")
        self.client.post(f"/auth/follow/{self.u2.id}/")

    def test_feed_contains_followed_post(self):
        r = self.client.get("/api/posts/feed/")
        self.assertEqual(r.status_code, 200)
        data = r.data
        # if paginated, data['results']; else data is list
        results = data.get("results", data)
        self.assertTrue(any(item["title"] == "hi" for item in results))
