from django.shortcuts import render
from django.views.generic import DetailView
from .models import Book, Library  # Must explicitly include Library


def list_books(request):
    """Function-based view that lists all books."""
    books = Book.objects.all()
    return render(request, "relationship_app/list_books.html", {"books": books})


class LibraryDetailView(DetailView):
    """Class-based view for displaying a specific library and its books."""

    model = Library
    template_name = "relationship_app/library_detail.html"
    context_object_name = "library"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        library = self.get_object()
        context["books"] = library.books.all()
        return context
