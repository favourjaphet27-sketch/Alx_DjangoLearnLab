This is the initial setup for the LibraryProject Django application. It includes the default configuration files and project structure.

# Security Features Implemented

## Secure Settings

- DEBUG set to False for production deployments.
- Enabled XSS, content sniffing, and frame protection:
  - SECURE_BROWSER_XSS_FILTER
  - SECURE_CONTENT_TYPE_NOSNIFF
  - X_FRAME_OPTIONS
- Cookies restricted to HTTPS:
  - CSRF_COOKIE_SECURE
  - SESSION_COOKIE_SECURE

## CSRF Protection

All POST forms include `{% csrf_token %}` to prevent CSRF attacks.

## SQL Injection Protection

User inputs are validated using Django forms.  
All queries use Django ORM to ensure parameterized queries.

## Content Security Policy (CSP)

Configured using `django-csp` middleware to restrict allowed content sources and reduce XSS risk.

## Testing

- Verified CSRF tokens appear in all forms.
- Tested form inputs with unsafe characters to confirm sanitization.
- Ensured CSP headers appear in browser response.
