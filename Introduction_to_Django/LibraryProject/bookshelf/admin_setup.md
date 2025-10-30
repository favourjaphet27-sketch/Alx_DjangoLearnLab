# Admin Integration for Book Model

Imported the Book model into 'bookshelf/admin.py'.
Created a 'BookAdmin' class to customize admin display:

- 'list_display' shows title, author, and publication_year
- 'search_fields' enables search by title and author
- 'list_filter' adds a filter by publication_year.

Registered the Book model with the admin using 'admin.site.register(Book, BookAdmin)'.
Verified setup by running the server and checking the Books section in the admin interface.
