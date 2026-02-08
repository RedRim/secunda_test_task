"""
зависимости для FastAPI
"""
from fastapi import Header, HTTPException, status

from app.config import get_config


async def verify_api_key(x_api_key: str = Header(...)):
    """
    проверка API ключа в заголовке запроса
    """
    if x_api_key != get_config().settings.api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API Key"
        )
    return x_api_key
