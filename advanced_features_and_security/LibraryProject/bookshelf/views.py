from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import permission_required
from .models import Book
from .forms import BookForm
from django import forms
from django.middleware.security import SecurityMiddleware
from django.utils.decorators import decorator_from_middleware
from .forms import ExampleForm


# Create your views here.
@permission_required("bookshelf.can_create", raise_exception=True)
def create_book(request):
    if request.method == "POST":
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("list_books")
        else:
            form = BookForm()

    return render(request, "bookshelf/create_book.html", {"form": form})


@permission_required("bookshelf.can_view", raise_exception=True)
def list_books(request):
    books = Book.objects.all()
    return render(request, "bookshelf/list_books.html")


@permission_required("bookshelf.can_edit", raise_exception=True)
def edit_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == "POST":
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect("list_books")
    else:
        form = BookForm(instance=book)
    return render(request, "bookshelf/edit_book.html", {"form": form})


# Delete a book
@permission_required("bookshelf.can_delete", raise_exception=True)
def delete_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == "POST":
        book.delete()
        return redirect("list_books")
    return render(request, "bookshelf/delete_book.html", {"book": book})


def add_csp_header(get_response):
    def middleware(request):
        response = get_response(request)
        response["Content-Security-Policy"] = "default-src 'self'"
        return response

    return middleware


@decorator_from_middleware(add_csp_header)
def book_list(request):
    books = Book.objects.all()
    context = {"books": books}
    return render(request, "bookshelf/book_list.html", context)


class SearchForm(forms.Form):
    q = forms.CharField(max_length=100)

    def search_books(request):
        form = SearchForm(request.GET)
        books = []
        if form.is_valid():
            query = form.cleaned_data["q"]
            books = Book.objects.filter(title__icontains=query)

        return render(request, "bookshelf/search.html", {"form": form, "books": books})


def example_form_view(request):
    form = ExampleForm()
    return render(request, "bookshelf/form_example.html", {"form": form})
