# app/core/exceptions.py
from fastapi import Request
from fastapi.responses import JSONResponse

class AppException(Exception):
    def __init__(self, message: str, status_code: int = 400):
        self.message = message
        self.status_code = status_code

class SessionNotFoundException(Exception):
    pass

class RIASECNotCompletedException(Exception):
    pass

class AIProcessingException(Exception):
    pass

# Exception handlers
def session_not_found_handler(request, exc):
    return JSONResponse(
        status_code=404,
        content={"error": "session_not_found", "message": str(exc)}
    )

async def app_exception_handler(request: Request, exc: AppException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.message,
            "path": request.url.path
        }
    )
