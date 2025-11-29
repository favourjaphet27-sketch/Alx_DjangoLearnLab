from django.shortcuts import render
from .models import Book
from rest_framework import generics, filters
from .serializers import BookSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django_filters import rest_framework


# Create your views here.
class BookListView(generics.ListAPIView):
    # Returns a list of books. Accessible to anyone(read-only).
    queryset = Book.objects.all()
    serializer = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["title", "author", "publication_year"]
    search_fields = ["title", "author"]
    ordering_fields = ["title", "publication_year"]


class BookDetailView(generics.RetrieveAPIView):
    # Returns a single book by it's ID. Accessible to everyone(read-only).
    queryset = Book.objects.all()
    serializer = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class BookCreateView(generics.CreateAPIView):
    # Allows authenticated users to create a new book
    queryset = Book.objects.all()
    serializer = BookSerializer
    permission_classes = [IsAuthenticated]


class BookUpdateView(generics.UpdateAPIView):
    # Allows full updates with PUT and partial updates with PATCH
    queryset = Book.objects.all()
    serializer = BookSerializer
    permission_classes = [IsAuthenticated]


class BookDeleteView(generics.DestroyAPIView):
    queryset = Book.objects.all()
    serializer = BookSerializer
    permission_classes = [IsAuthenticated]
