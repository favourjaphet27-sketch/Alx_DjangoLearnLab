View Configuration

Each view is built on Django REST Framework’s generic views. They provide default CRUD behavior, and I extended them only where needed.

ListView and DetailView
These use the default list and retrieve behavior. They don’t need custom logic.
Read-only access is allowed for everyone.

CreateView and UpdateView
These views use DRF’s lifecycle hooks.
perform_create adds extra rules before saving a new book.
perform_update adds permission checks and additional validation before updating a book.
Only authenticated users can write data.

DeleteView
Standard delete behavior, restricted to authenticated users only.

Custom Hooks

The project uses these DRF hooks:

perform_create
Runs after serializer validation but before saving.
Useful for extra validation or attaching extra data.

perform_update
Works the same way but during updates.
This project uses it to apply custom permission logic.
