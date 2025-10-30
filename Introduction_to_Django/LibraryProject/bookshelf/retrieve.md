# Retrieve Operations

'''python
from bookshelf.models import Book
Book.objects.all().values()

# Output: [{'id': 1, 'title': '1984', 'author': 'George Orwell', 'publication_year': 1949}]
