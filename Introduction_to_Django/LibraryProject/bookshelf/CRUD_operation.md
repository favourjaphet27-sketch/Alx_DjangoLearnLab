# Output Operations

# Create

'''python
from bookshelf.models import Book
book = Book.objects.create(title='1984', author='George Orwell', publication_year=1949)
book

# Output: <Book: 1984>

# Retrieve Operations

'''python
from bookshelf.models import Book
Book.objects.all().values()

# Output: [{'id': 1, 'title': '1984', 'author': 'George Orwell', 'publication_year': 1949}]

# Update

'''python
book = Book.objects.get(title='1984')
book.title = "Nineteen Eighty-Four"
book.save()
book

# Output: <Book: Nineteen Eighty-Four>

# Delete

'''python
Book.delete()
Book.objects.all()

# Output: (1, {'bookshelf.Book': 1}) and then an empty Queryset[]
