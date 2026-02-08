from typing import TypeVar
from app.schemas.response import APIResponse

T = TypeVar("T")

def success_response(data: T = None, message: str = "Request successfull") -> APIResponse[T]:
    return APIResponse[T](status = "success", data=data, message=message, success=True)

def error_response(error: str, message: str = 'Request failed') -> APIResponse[T]:
    return APIResponse[None](status='error', error=error, message=message, success=False)