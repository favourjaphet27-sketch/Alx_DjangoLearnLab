from django.urls import path
from .views import list_books
from .views import (
    LibraryDetailView,
    add_book,
    edit_book,
    delete_book,
    admin_view,
    librarian_view,
    member_view,
    UserLoginView,
    UserLogoutView,
    register,
)

urlpatterns = [
    path("books/", list_books, name="list_books"),  # function based viewpath
    path(
        "library/<int:pk>/", LibraryDetailView.as_view(), name="library_detail"
    ),  # class-based view
    path("add_book/", add_book, name="add_book"),
    path("edit_book/<int:pk>/", edit_book, name="edit_book"),
    path("delete_book/<int:pk>/", delete_book, name="delete_book"),
    # Authentication views
    path("register/", register, name="register"),
    path(
        "login/",
        UserLoginView.as_view(template_name="relationship_app/login.html"),
    ),
    path(
        "logout/",
        UserLogoutView.as_view(template_name="relationship_app/logout.html"),
    ),
    # role based views
    path("admin/", admin_view, name="admin_view"),
    path("librarian/", librarian_view, name="librarian_view"),
    path("member/", member_view, name="member_view"),
]
