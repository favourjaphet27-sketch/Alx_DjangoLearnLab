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
    CommentListView,
    CommentCreateView,
    CommentUpdateView,
    CommentDeleteView,
    PostByTagListView,
    SearchResultsView,
)

app_name = "blog"

urlpatterns = [
    path("", PostListView.as_view(), name="home"),
    path("register/", RegisterView.as_view(), name="register"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("login/", UserLoginView.as_view(), name="login"),
    path("logout/", UserLogoutView.as_view(), name="logout"),
    path("posts/", PostListView.as_view(), name="post-list"),
    path("posts/new/", PostCreateView.as_view(), name="new-post"),
    path("posts/<int:pk>/", PostDetailView.as_view(), name="post-detail"),
    path("posts/<int:pk>/edit/", PostUpdateView.as_view(), name="edit-post"),
    path("posts/<int:pk>/delete/", PostDeleteView.as_view(), name="delete-post"),
    path(
        "posts/<int:post_pk>/comments/", CommentListView.as_view(), name="comment-list"
    ),
    path(
        "posts/<int:post_pk>/comments/new/",
        CommentCreateView.as_view(),
        name="comment-create",
    ),
    path("comments/<int:pk>/edit/", CommentUpdateView.as_view(), name="comment-edit"),
    path(
        "comments/<int:pk>/delete/", CommentDeleteView.as_view(), name="comment-delete"
    ),
    path("tags/<slug:tag_slug>/", PostByTagListView.as_view(), name="posts-by-tag"),
    path("search/", SearchResultsView.as_view(), name="post-search"),
]
