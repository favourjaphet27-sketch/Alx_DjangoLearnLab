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
    path("post/", PostListView.as_view(), name="post-list"),
    path("post/new/", PostCreateView.as_view(), name="new-post"),
    path("post/<int:pk>/", PostDetailView.as_view(), name="post-detail"),
    path("post/<int:pk>/edit/", PostUpdateView.as_view(), name="edit-post"),
    path("post/<int:pk>/delete/", PostDeleteView.as_view(), name="delete-post"),
    path("post/<int:pk>/comment/", CommentListView.as_view(), name="comment-list"),
    path(
        "post/<int:pk>/comments/new/",
        CommentCreateView.as_view(),
        name="comment-create",
    ),
    path("comment/<int:pk>/update/", CommentUpdateView.as_view(), name="comment-edit"),
    path(
        "comment/<int:pk>/delete/", CommentDeleteView.as_view(), name="comment-delete"
    ),
    path("tags/<slug:tag_slug>/", PostByTagListView.as_view(), name="posts-by-tag"),
    path("search/", SearchResultsView.as_view(), name="post-search"),
]
