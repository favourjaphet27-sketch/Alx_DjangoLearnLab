from django.urls import path, include
from .views import BookList
from rest_framework.routers import DefaultRouter
from .views import BookViewSet

router = DefaultRouter()
router.register(r"books_all", BookViewSet, basename="book_all")

urlpatterns = [
    # route for the BookList view (ListAPIView)
    path("books/", BookList.as_view(), name="book-list"),
    # Include the router URLs for BookViewSet
    path("", include("router.urls")),
]
