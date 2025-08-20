from typing import Callable
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from jose import jwt, JWTError
from .config import settings
from .database import SessionLocal
from .models import User

PROTECTED_PREFIXES = ("/messages", "/me")

class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable[[Request], Response]) -> Response:
        path = request.url.path
        need_auth = path.startswith(PROTECTED_PREFIXES)
        token = None
        auth = request.headers.get("authorization") or request.headers.get("Authorization")
        if auth and auth.lower().startswith("bearer "):
            token = auth.split(" ", 1)[1].strip()

        user = None
        if token:
            try:
                payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
                user_id = int(payload.get("sub"))
                with SessionLocal() as db:
                    user = db.query(User).filter(User.id == user_id).first()
            except (JWTError, ValueError):
                user = None

        request.state.user = user

        if need_auth and user is None:
            from fastapi.responses import JSONResponse
            return JSONResponse({"detail": "Not authenticated"}, status_code=401)

        return await call_next(request)
