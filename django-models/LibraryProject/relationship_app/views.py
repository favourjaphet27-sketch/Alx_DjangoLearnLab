from django.shortcuts import render, redirect
from django.views.generic import DetailView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import login
from .models import Book, Library
from .forms import UserRegisterForm

# Function-based view: list all books
def list_books(request):
    """Function-based view that lists all books."""
    books = Book.objects.all()
    return render(request, 'relationship_app/list_books.html', {'books': books})

# Class-based view: show library details
class LibraryDetailView(DetailView):
    """Class-based view for displaying a specific library and its books."""
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        library = self.get_object()
        context['books'] = library.books.all()
        return context

# User registration view
def register_view(request):
    """Handle user registration."""
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('list_books')
    else:
        form = UserRegisterForm()
    return render(request, 'relationship_app/register.html', {'form': form})

# User login view
class UserLoginView(LoginView):
    template_name = 'relationship_app/login.html'

# User logout view
class UserLogoutView(LogoutView):
    template_name = 'relationship_app/logout.html'
