"""Session management using itsdangerous signed cookies."""
import os
import json
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired
from typing import Optional
from fastapi import Request, Response

# Session signing key: read from SESSION_SECRET environment variable.
# DEV_ONLY_FALLBACK is strictly for offline local evaluation; provide SESSION_SECRET in production.
SESSION_SECRET = os.getenv("SESSION_SECRET") or os.getenv("SECRET_KEY") or "DEV_ONLY_UNSECURE_SECRET_CHANGE_FOR_PRODUCTION"
COOKIE_NAME = "schemefinder_session"
MAX_AGE = 86400 * 7  # 7 days

serializer = URLSafeTimedSerializer(SESSION_SECRET, salt="schemefinder-session-salt")

DEFAULT_SESSION = {
    "profile": {},
    "owned_docs": [],
    "lang": "en"
}

def get_session(request: Request) -> dict:
    cookie = request.cookies.get(COOKIE_NAME)
    if not cookie:
        return dict(DEFAULT_SESSION)
    try:
        data = serializer.loads(cookie, max_age=MAX_AGE)
        # Ensure default keys
        if not isinstance(data, dict):
            return dict(DEFAULT_SESSION)
        if "profile" not in data:
            data["profile"] = {}
        if "owned_docs" not in data:
            data["owned_docs"] = []
        if "lang" not in data:
            data["lang"] = "en"
        return data
    except (BadSignature, SignatureExpired, Exception):
        return dict(DEFAULT_SESSION)

def set_session(response: Response, data: dict, request: Request = None):
    token = serializer.dumps(data)
    secure = False
    if request:
        proto = request.headers.get("x-forwarded-proto", request.url.scheme)
        secure = (proto == "https")
    elif os.getenv("VERCEL") or os.getenv("RENDER") or os.getenv("HTTPS") == "on":
        secure = True

    response.set_cookie(
        key=COOKIE_NAME,
        value=token,
        max_age=MAX_AGE,
        httponly=True,
        samesite="lax",
        path="/",
        secure=secure
    )

def clear_session(response: Response):
    response.delete_cookie(key=COOKIE_NAME, path="/")
