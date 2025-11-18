from django.shortcuts import render
from .serializers import BookSerializer
from rest_framework import generics
from .models import Book
from rest_framework import viewsets


# Create your views here.
class BookList(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer = BookSerializer


class BookViewSet(viewsets.ModelViewSet):
    query = Book.objects.all()
    serializer = BookSerializer
