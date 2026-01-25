from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

class CookieToHeaderMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Revisamos si la cookie existe
        token = request.cookies.get("access_token")
        if token:
            # Insertamos el header Authorization internamente
            # ⚠️ _list es la forma de modificar headers de Starlette
            request.headers.__dict__["_list"].append(
                (b"authorization", f"Bearer {token}".encode())
            )
        response = await call_next(request)
        return response