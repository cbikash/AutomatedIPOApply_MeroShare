from typing import Generic, Optional,TypeVar
from pydantic import BaseModel
from pydantic.generics import GenericModel

T = TypeVar("T")

class APIResponse(GenericModel, Generic[T]):
    status: str
    data: Optional[T] = None
    message: Optional[str] = None
    error: Optional[str] = None
    success: bool = True