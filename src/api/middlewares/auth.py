from fastapi import Request, status
from fastapi.responses import JSONResponse

from utils.exceptions import UnauthorizedError

from services.auth import AuthService

from jwt import ExpiredSignatureError


async def auth_middleware(request: Request, call_next, auth_service: AuthService = AuthService()):
    try:
        if request.url.path in ["/auth", "/users/register", "/docs", "/openapi.json"]:
            return await call_next(request)
        
        auth_cookie = request.cookies.get("auth")
        if not auth_cookie:
            raise UnauthorizedError("Unauthorized")
        
        token_data = auth_service.get_user(auth_cookie)
        
        request.state.user = {
            "user_id": int(token_data.user_id)
        }
        
        return await call_next(request)
    
    except (UnauthorizedError, ExpiredSignatureError):
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"detail": "Unauthorized"}
        )