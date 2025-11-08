import os
import django

from relationship_app import Author, Book, Library, Librarian


# Query all books by a specific author
def get_books_by_author(author_name):
    author = Author.objects.get(name=author_name)
    return author.books.all()


# Lists all books in a library
def get_books_in_library(library_name):
    library = Library.objects.get(name=library_name)
    return library.books.all()


# Retrieve the librarian for a library
def get_librarian_for_library(library_name):
    library = Library.objects.get(name=library_name)
    return library.librarian


# Example Usage
if __name__ == "__main__":
    print("Books by J.K. Rowling:", get_books_by_author("J.K. Rowling"))
    print("Books in Central Library:", get_books_in_library("Central Library"))
    print("Librarian of Central Library:", get_librarian_for_library("Central Library"))
