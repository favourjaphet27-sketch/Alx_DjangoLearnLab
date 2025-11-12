from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import permission_required
from .models import UserProfile
from django.views.generic.detail import DetailView
from .models import Library, Book


# List all books
def list_books(request):
    books = Book.objects.all()
    return render(request, "relationship_app/list_books.html", {"books": books})


# Library detail view
class LibraryDetailView(DetailView):
    model = Library
    template_name = "relationship_app/library_detail.html"
    context_object_name = "library"

    def get_context_data(self, **kwargs):
        # kwargs helps you accept whatever context django's parent class is sending in
        context = super().get_context_data(**kwargs) 
        # super is like saying get whatever context django had so you can add more to it
        library = self.get_object()
        context["books"] = library.books.all()
        return context


# Book CRUD views with permissions
@permission_required("relationship_app.can_add_book", raise_exception=True)
def add_book(request):
    if request.method == "POST":
        title = request.POST.get("title")
        author_id = request.POST.get("author")
        Book.objects.create(title=title, author_id=author_id)
        return redirect("list_books")
    return render(request, "relationship_app/add_book.html")


# Edit a book (requires permission)
@permission_required("relationship_app.can_change_book", raise_exception=True)
def edit_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == "POST":
        book.title = request.POST.get("title")
        book.author_id = request.POST.get("author")
        book.save()
        return redirect("list_books")
    return render(request, "relationship_app/edit_book.html", {"book": book})


# Delete a book (requires permission)
@permission_required("relationship_app.can_delete_book", raise_exception=True)
def delete_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == "POST":
        book.delete()
        return redirect("list_books")
    return render(request, "relationship_app/delete_book.html", {"book": book})


# Register view
def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful!")
            return redirect("login")
    else:
        form = UserCreationForm()
    return render(request, "relationship_app/register.html", {"form": form})


# Login view
class UserLoginView(LoginView):
    template_name = "relationship_app/login.html"


class UserLogoutView(LogoutView):
    template_name = "relationship_app/logout.html"


from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from .models import UserProfile


# Function to check roles
def is_admin(user):
    return (
        user.is_authenticated
        and hasattr(user, "userprofile")
        and user.userprofile.role == "Admin"
    )


def is_librarian(user):
    return (
        user.is_authenticated
        and hasattr(user, "userprofile")
        and user.userprofile.role == "Librarian"
    )


def is_member(user):
    return (
        user.is_authenticated
        and hasattr(user, "userprofile")
        and user.userprofile.role == "Member"
    )


@user_passes_test(is_admin)
def admin_view(request):
    """View accessible only by Admin users."""
    return render(request, "relationship_app/admin_view.html")


@user_passes_test(is_librarian)
def librarian_view(request):
    """View accessible only by Librarian users."""
    return render(request, "relationship_app/librarian_view.html")


@user_passes_test(is_member)
def member_view(request):
    """View accessible only by Member users."""
    return render(request, "relationship_app/member_view.html")
