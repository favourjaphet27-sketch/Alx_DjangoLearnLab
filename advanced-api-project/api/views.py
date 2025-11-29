from django.shortcuts import render
from .models import Book
from rest_framework import generics, permissions
from .serializers import BookSerializer
from rest_framework.exceptions import ValidationError, PermissionDenied


# Create your views here.
class BookListView(generics.ListAPIView):
    # Returns a list of books. Accessible to anyone(read-only).
    queryset = Book.objects.all()
    serializer = BookSerializer
    permission_classes = [permissions.AllowAny]


class BookDetailView(generics.RetrieveAPIView):
    # Returns a single book by it's ID. Accessible to everyone(read-only).
    queryset = Book.objects.all()
    serializer = BookSerializer
    permission_classes = [permissions.AllowAny]


class BookCreateView(generics.CreateAPIView):
    # Allows authenticated users to create a new book
    queryset = Book.objects.all()
    serializer = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        year = serializer.validated_data["publication_year"]
        if year < 1900:
            raise ValidationError("Publication year must be 1900 or later.")
        serializer.save()


class BookUpdateView(generics.UpdateAPIView):
    # Allows full updates with PUT and partial updates with PATCH
    queryset = Book.objects.all()
    serializer = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_update(self, serializer):
        year = serializer.validated_data["publication_year"]
        if year < 2000 and not self.request.user.is_staff:
            raise PermissionDenied("Only staff can edit books older than year 2000")
        serializer.save()


class BookDeleteView(generics.DestroyAPIView):
    queryset = Book.objects.all()
    serializer = BookSerializer
    permission_classes = [permissions.IsAuthenticated]
