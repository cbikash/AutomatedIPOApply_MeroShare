import httpx
import logging
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)

def safe_http_request(
    method: str,
    url: str,
    *,
    json: Optional[Dict[str, Any]] = None,
    data: Optional[Dict[str, Any]] = None,
    headers: Optional[Dict[str, str]] = None,
    params: Optional[Dict[str, Any]] = None,
    timeout: float = 10.0,
    auth: Optional[bool] = False,
) -> Dict[str, Any]:
    """
    Generic HTTP request that NEVER raises an exception.
    Always returns a unified response dict.
    """

    try:
        with httpx.Client(timeout=timeout) as client:
            response = client.request(
                method=method.upper(),
                url=url,
                json=json,
                data=data,
                headers=headers,
                params=params
            )

        # Non-success HTTP status
        if response.status_code >= 400:
            return {
                "success": False,
                "status_code": response.status_code,
                "message": "HTTP request failed",
                "detail": response.text
            }

        # Safe JSON parse
        try:
            data = {
                "success": True,
                "status_code": response.status_code,
                "data": response.json(),
            }

            if(auth):
               data['auth'] = response.headers.get("authorization")
            
            return data
        
        except ValueError:
            return {
                "success": True,
                "status_code": response.status_code,
                "data": response.text
            }

    except httpx.TimeoutException:
        return {
            "success": False,
            "status_code": 408,
            "message": "Request timeout"
        }

    except httpx.RequestError as e:
        return {
            "success": False,
            "status_code": 503,
            "message": "Service unavailable",
            "detail": str(e)
        }

    except Exception as e:
        logger.exception("Unexpected error in safe_http_request")
        return {
            "success": False,
            "status_code": 500,
            "message": "Unexpected internal error"
        }
