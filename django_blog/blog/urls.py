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
    TagPostListView,
    SearchResultsView,
)

app_name = "blog"

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("login/", UserLoginView.as_view(), name="login"),
    path("logout/", UserLogoutView.as_view(), name="logout"),
    path("post/", PostListView.as_view(), name="post-list"),
    path("post/new/", PostCreateView.as_view(), name="new-post"),
    path("post/<int:pk>", PostDetailView.as_view(), name="post-detail"),
    path("post/<int:pk>/update/", PostUpdateView.as_view(), name="post-edit"),
    path("post/<int:pk>/delete/", PostDeleteView.as_view(), name="delete-post"),
    path(
        "post/<int:pk>/comments/new/",
        CommentCreateView.as_view(),
        name="comment-create",
    ),
    path(
        "comment/<int:pk>/update/",
        CommentUpdateView.as_view(),
        name="comment-update",
    ),
    path(
        "comment/<int:pk>/list/",
        CommentListView.as_view(),
        name="comment-list",
    ),
    path(
        "comment/<int:pk>/delete/",
        CommentDeleteView.as_view(),
        name="comment-delete",
    ),
    path("tags/<str:tag_name>/", TagPostListView.as_view(), name="posts-by-tag"),
    path("search/", SearchResultsView.as_view(), name="post-search"),
]
