"""
Do read:
    1. https://docs.djangoproject.com/en/3.1/ref/settings/#sessions
    2. https://developer.mozilla.org/en-US/docs/Web/HTTP/Cookies
"""
SESSION_COOKIE_AGE = 1209600
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'
SESSION_COOKIE_SECURE = False
CSRF_USE_SESSIONS = True