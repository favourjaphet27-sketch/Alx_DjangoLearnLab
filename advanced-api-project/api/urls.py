from django.urls import path
from .views import (
    BookListView,
    BookDetailView,
    BookDeleteView,
    BookCreateView,
    BookUpdateView,
)

urlpatterns = [
    path("books/", BookListView.as_view(), name="book-list"),
    path("books/<int:pk>/", BookDetailView.as_view(), name="book-detail"),
    path("book/create/", BookCreateView.as_view(), name="book-create"),
    path("book/update/<int:pk>/", BookUpdateView.as_view(), name="book-update"),
    path("book/delete/<int:pk>/", BookDeleteView.as_view(), name="book-delete"),
]
