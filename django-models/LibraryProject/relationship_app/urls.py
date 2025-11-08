from django.urls import path
from . import views

urlpatterns = [
    path("books/", views.list_books, name="list_books"), #function based view
    path("library/<int:pk>/", views.LibraryDetailView.as_view(), name="library_detail"), #class-based view
    path('register/', views.register_view, name='register'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', views.UserLogoutView.as_view(), name='logout'),
]
