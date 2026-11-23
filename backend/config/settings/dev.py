"""
Development settings for the project.
"""

from .base import *


DEBUG = True
ENABLE_API_DOCS = True

ALLOWED_HOSTS = env.list(
    "ALLOWED_HOSTS",
    default=["localhost", "127.0.0.1", "[::1]"]
)

_FRONTEND_ORIGINS = ["http://localhost:8000"]

CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOWED_ORIGINS = _FRONTEND_ORIGINS

CORS_ALLOW_CREDENTIALS = True

CSRF_TRUSTED_ORIGINS = env.list(
    "CSRF_TRUSTED_ORIGINS",
    default=_FRONTEND_ORIGINS
)

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# Browsable API + JSON, and relaxed throttling for development/testing
REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'] = (
    'rest_framework.renderers.BrowsableAPIRenderer',
    'rest_framework.renderers.JSONRenderer',
)
REST_FRAMEWORK['DEFAULT_THROTTLE_RATES'] = {
    'anon': '1000/day',
    'user': '1000/day'
}

# if you want to add debug toolbar
#INSTALLED_APPS += [
#    "debug_toolbar",
#]
#MIDDLEWARE += [
#    "debug_toolbar.middleware.DebugToolbarMiddleware",
#]
#INTERNAL_IPS = ["127.0.0.1"]
