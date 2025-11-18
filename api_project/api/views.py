from django.shortcuts import render
from .serializers import BookSerializer
from rest_framework import generics
from .models import Book
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

# All API views use TokenAuthentication and require a valid token,
# because DEFAULT_PERMISSION_CLASSES applies globally.
# Example header for requests:
# Authorization: Token <your_token_here>


class BookList(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer = BookSerializer


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer = BookSerializer
    permission_classes = [IsAuthenticated]
