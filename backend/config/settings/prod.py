"""
Production settings for the project.
Verify before deployment: python manage.py check --deploy
"""

# Load the Production settings if docker isn't running.
from . import BASE_DIR, env
env.read_env(BASE_DIR / '.env.prod')


from django.utils.csp import CSP
from .base import *


DEBUG = False
ENABLE_API_DOCS = False

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS")


# Database

DATABASES["default"]["OPTIONS"] = {
    "sslmode": "require"
}


# Cache

# Redis cache configuration (wrote this out incase I ever need it)
#CACHES = {
#    "default": {
#        "BACKEND": "django.core.cache.backends.redis.RedisCache",
#        "LOCATION": env("REDIS_URL"),
#        "KEY_PREFIX": env("CACHE_KEY_PREFIX"),
#    }
#}


# CORS settings for production

CORS_ALLOW_ALL_ORIGINS = False 
CORS_ALLOWED_ORIGINS = env.list("CORS_ALLOWED_ORIGINS")
CORS_ALLOW_CREDENTIALS = True

CSRF_TRUSTED_ORIGINS = env.list("CSRF_TRUSTED_ORIGINS", default=[]) # cookie based authentication


# HTTPS / SSL 

SECURE_SSL_REDIRECT = True
# Don't need HTTPS for health checks
SECURE_REDIRECT_EXEMPT = [r'^health/$']

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
USE_X_FORWARDED_HOST = True


# Cookies (session and CSRF)

SESSION_COOKIE_SECURE = True 
SESSION_COOKIE_HTTPONLY = True 
SESSION_COOKIE_SAMESITE = 'Lax' 

CSRF_COOKIE_SECURE = True 
CSRF_COOKIE_HTTPONLY = False 
CSRF_COOKIE_SAMESITE = 'Lax'


# HSTS

SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = False # Note to self: only turn this to true when you are confident that your site is ready for HSTS preload


# Security headers

SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = "DENY"
SECURE_REFERRER_POLICY = "same-origin"
SECURE_CROSS_ORIGIN_OPENER_POLICY = "same-origin"

SILENCED_SYSTEM_CHECKS = ["security.W004", "security.W008"]  # HSTS + redirect live in nginx

_CSP_POLICY = {
    "default-src": [CSP.NONE],
    "script-src": [CSP.SELF],
    "style-src": [CSP.SELF],
    "img-src": [CSP.SELF, "data:"],
    "font-src": [CSP.SELF],
    "connect-src": [CSP.SELF],
    "form-action": [CSP.SELF],
    "base-uri": [CSP.NONE],
    "frame-ancestors": [CSP.NONE],
}
_csp_report_uri = env("CSP_REPORT_URI", default="")
if _csp_report_uri:
    _CSP_POLICY["report-uri"] = _csp_report_uri

if env.bool("CSP_ENFORCE", default=False):
    SECURE_CSP = _CSP_POLICY
else:
    SECURE_CSP_REPORT_ONLY = _CSP_POLICY


# Django Rest Framework

REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'] = (
    'rest_framework.renderers.JSONRenderer',
)
