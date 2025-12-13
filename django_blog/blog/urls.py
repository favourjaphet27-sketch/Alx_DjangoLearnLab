from django.urls import path
from .views import (
    RegisterView,
    ProfileView,
    UserLoginView,
    UserLogoutView,
    PostListView,
    PostCreateView,
    PostUpdateView,
    PostDetailView,
    PostDeleteView,
    CommentCreateView,
    CommentDeleteView,
    CommentListView,
    CommentUpdateView,
)

app_name = "blog"

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("login/", UserLoginView.as_view(), name="login"),
    path("logout/", UserLogoutView.as_view(), name="logout"),
    path("posts/", PostListView.as_view(), name="post-list"),
    path("posts/new/", PostCreateView.as_view(), name="new-post"),
    path("posts/<int:pk>", PostDetailView.as_view(), name="post-detail"),
    path("posts/<int:pk>/update/", PostUpdateView.as_view(), name="post-edit"),
    path("posts/<int:pk>/delete/", PostDeleteView.as_view(), name="delete-post"),
    path(
        "posts/<int:post_id>/comments/new/",
        CommentCreateView.as_view(),
        name="comment-create",
    ),
    path(
        "posts/<int:post_id>/comments/update/",
        CommentUpdateView.as_view(),
        name="comment-update",
    ),
    path(
        "posts/<int:post_id>/comments/list/",
        CommentListView.as_view(),
        name="comment-list",
    ),
    path(
        "posts/<int:post_id>/comments/delete/",
        CommentDeleteView.as_view(),
        name="comment-delete",
    ),
]
