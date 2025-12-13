from rest_framework.routers import DefaultRouter
from .views import PostViewSet, CommentViewSet, FeedView, LikePostView, UnlikePostView
from django.urls import path, include

router = DefaultRouter()
router.register("posts", PostViewSet, basename="post")
router.register("comments", CommentViewSet, basename="comment")

urlpatterns = [
    path("", include(router.urls)),
    path("feed/", FeedView.as_view(), name="feed"),
    path("<int:pk>/like/", LikePostView.as_view(), name="like-post"),
    path("<int:pk>/unlike/", UnlikePostView.as_view(), name="unlike-post"),
]
