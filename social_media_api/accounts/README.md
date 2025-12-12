# Accounts — Setup & Quick Guide

A concise guide to the accounts app: setup, registering users, authentication, and a short user-model overview.

## Setup

1. Ensure the app is listed in INSTALLED_APPS (settings.py):
   - `"accounts"` or the app path used in your project.
2. Apply migrations:
   - From project root: `python manage.py makemigrations` then `python manage.py migrate`
3. (Optional) Create a superuser:
   - `python manage.py createsuperuser`
4. Static & media (if profiles have images):
   - Set `MEDIA_ROOT` and `MEDIA_URL` in settings.py. During development serve media via urlpatterns.

## Registering a user

- URL: `/register/` (or the route defined in urls.py).
- Form: a registration form based on `UserCreationForm` that collects username, email, password1 and password2.
- Flow:
  1. User fills and POSTs the form.
  2. View validates and saves the User.
  3. View may log the user in automatically with `login(request, user)`.
  4. Redirects to profile or `LOGIN_REDIRECT_URL`.

## Authenticating users

- Login: `/login/` — typically uses Django's `LoginView`.
- Logout: `/logout/` — typically uses Django's `LogoutView`.
- Recommended settings:
  - `LOGIN_URL = "accounts:login"` (or `"login"` depending on URL include)
  - `LOGIN_REDIRECT_URL = "profile"` (or your chosen route)

## Viewing & editing profile

- Protected view (requires authentication): `/profile/`.
- Use two forms on the same page:
  - `UserUpdateForm` (ModelForm) — edits User fields (username, email).
  - `ProfileUpdateForm` (ModelForm) — edits Profile fields (image, bio, etc.).
- Template must include `enctype="multipart/form-data"` when handling file uploads.

## User model overview

- Authentication: default `django.contrib.auth.models.User` is commonly used for credentials.
- Profile: extra info (avatar, bio) lives in a separate `Profile` model linked via OneToOneField to User.
- Profile creation: use a `post_save` signal to create a Profile when a User is created, or ensure views call `Profile.objects.get_or_create(user=...)`.

## Tips & best practices

- Keep registration forms for creation only; use ModelForm for updates.
- Validate email uniqueness in registration/update forms.
- Protect edit/delete operations with `LoginRequiredMixin` and permission checks (`UserPassesTestMixin`).
- Use Django messages to show success/error feedback.
- In production, serve media files with a proper storage backend and configure `STATIC_ROOT`/`collectstatic`.

## Endpoints for following

Follow / Unfollow

- POST /auth/follow/<user_id>/ -> follow user
- POST /auth/unfollow/<user_id>/ -> unfollow user
- GET /auth/following/ -> list users you follow

Feed

- GET /api/posts/feed/ -> paginated posts from users you follow, newest first
  Authorization: Token <token>
