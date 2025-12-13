# Social Media API

## Overview

The Social Media API is a RESTful backend application built with **Django** and **Django REST Framework**.  
It provides core social media features such as authentication, posts, comments, follows, likes, feeds, and notifications.

The project focuses on clean architecture, proper permissions, and scalable API design.

## Tech Stack

- Python
- Django
- Django REST Framework
- MySQL (development database)
- Token Authentication
- Gunicorn (production)
- Nginx (production)

## Project Structure

social_media_api/
│
├── accounts/ # Custom user model, authentication, follows
├── posts/ # Posts, comments, likes, feed
├── notifications/ # Notification system
├── social_media_api/ # Project settings
├── manage.py
└── requirements.txt

## Features

### Authentication

- User registration
- Login with token generation
- Token-based authentication for protected endpoints

### Posts

- Create, retrieve, update, and delete posts
- Pagination and search by title or content
- Permissions ensure only authors can edit or delete their posts

### Comments

- Comment on posts
- Edit and delete own comments only

### Follow System

- Users can follow and unfollow other users
- Follow relationships are stored using a self-referential many-to-many field

### Feed

- Authenticated users can view a feed of posts
- Feed shows posts created by users they follow
- Posts are ordered by most recent first

### Likes

- Users can like and unlike posts
- Duplicate likes are prevented

### Notifications

- Users receive notifications when:
  - Someone follows them
  - Someone likes their post
  - Someone comments on their post
- Users can fetch their notifications through an API endpoint

## API Endpoints (Overview)

### Authentication

- `POST /api/accounts/register/`
- `POST /api/accounts/login/`

### Posts

- `GET /api/posts/`
- `POST /api/posts/`
- `GET /api/posts/<pk>/`
- `PUT /api/posts/<pk>/`
- `DELETE /api/posts/<pk>/`

### Comments

- `POST /api/comments/`
- `PUT /api/comments/<pk>/`
- `DELETE /api/comments/<pk>/`

### Follow System

- `POST /api/accounts/follow/<user_id>/`
- `POST /api/accounts/unfollow/<user_id>/`

### Feed

- `GET /api/posts/feed/`

### Likes

- `POST /api/posts/<pk>/like/`
- `POST /api/posts/<pk>/unlike/`

### Notifications

- `GET /api/notifications/`

---

## Permissions

- Only authenticated users can create posts, comments, likes, or follows
- Users can only modify or delete content they own
- Follow and unfollow actions apply only to the logged-in user

---

## Pagination and Filtering

- List endpoints use pagination to handle large datasets
- Posts can be searched by title or content using query parameters

---

## Database Configuration

The project uses **MySQL** for development.

Example configuration in `settings.py`:

```python
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "social_media_api",
        "USER": "your_db_username",
        "PASSWORD": "your_db_password",
        "HOST": "localhost",
        "PORT": "3306",
    }
}

## Deployment
- Production uses Gunicorn as the WSGI server
- Nginx is used as a reverse proxy
- Environment variables are used for sensitive settings
- Static files are collected using collectstatic
```
