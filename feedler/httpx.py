"""
Define how to get httpx client.
"""
from collections.abc import AsyncGenerator

from httpx import AsyncClient


async def get_httpx_client() -> AsyncGenerator[AsyncClient, None]:
    """
    Getter
    """
    httpx_client = AsyncClient()
    yield httpx_client
    await httpx_client.aclose()
