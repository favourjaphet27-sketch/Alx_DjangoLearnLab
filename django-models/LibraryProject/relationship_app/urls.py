from django.urls import path
from . import views

urlpatterns = [
    path("books/", views.list_books, name="list_books"),  # function based view
    path("register/", views.register, name="register"),
    path(
        "login/",
        views.UserLoginView.as_view(template_name="relationship_app/login.html"),
    ),
    path(
        "logout/",
        views.UserLogoutView.as_view(template_name="relationship_app/logout.html"),
    ),
    path(
        "library/<int:pk>/", views.LibraryDetailView.as_view(), name="library_detail"
    ),  # class-based view
]
