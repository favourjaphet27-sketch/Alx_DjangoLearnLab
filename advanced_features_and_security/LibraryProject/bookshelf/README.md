# Advanced Features and Security

This project contains two major features: a custom user model and a permission-based access control system.

## Custom User Model

The project replaces Django’s default User model with a CustomUser model.  
It extends AbstractUser and includes the following additional fields:

- date_of_birth
- profile_photo

A CustomUserManager class handles user creation and superuser creation.  
The project settings use this model through:

AUTH_USER_MODEL = "bookshelf.CustomUser"

The custom user model is registered in the admin using a custom admin class so the extra fields appear in the Django admin panel.

## Permissions and Groups

The Book model includes custom permissions:

- can_create
- can_edit
- can_delete
- can_view

These permissions are used to control access to specific views.  
Groups such as Viewers, Editors, and Admins can be created in Django admin and given the appropriate permissions.

Example views use permission checks such as:
@permission_required("bookshelf.can_create", raise_exception=True)

## How Access Control Works

1. Users are assigned to groups.
2. Groups contain the permissions needed for different actions.
3. Views check for the required permissions before allowing actions like creating or editing a book.

## Testing

You can create test users, assign them to different groups from Django admin, then log in and confirm that only users with the correct permissions can access restricted views.
