# Delete Operation

'''python
from bookshelf.models import Book
book = Book.objects.get(title="Nineteen Eighty-Four")
book.delete()

# Confirm Deletion

Book.objects.all()

# Output: <Queryset []>
