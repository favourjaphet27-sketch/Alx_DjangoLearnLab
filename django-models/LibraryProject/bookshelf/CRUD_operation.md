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
Book.objects.get
book

Output: <Book: 1984>

# Update

'''python
book = Book.objects.get(title="1984")
book.title = "Nineteen Eighty-Four"
book.save()
book

# Output: <Book: Nineteen Eighty-Four>

# Delete

'''python
book = Book.objects.get(title="Nineteen Eighty-Four")
Book.delete()

# Confirm Deletion

Book.objects.all()

# Output: <Queryset []>
