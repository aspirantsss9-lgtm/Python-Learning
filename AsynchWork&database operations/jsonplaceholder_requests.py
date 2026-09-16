from __future__ import annotations

from typing import Any

import aiohttp


USERS_DATA_URL = "https://jsonplaceholder.typicode.com/users"
POSTS_DATA_URL = "https://jsonplaceholder.typicode.com/posts"


async def fetch_json(url: str) -> list[dict[str, Any]]:
    """Fetch JSON data from the specified URL."""
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            response.raise_for_status()
            data = await response.json()

    return data


async def fetch_users_data() -> list[dict[str, Any]]:
    """Fetch users data from JSONPlaceholder."""
    return await fetch_json(USERS_DATA_URL)


async def fetch_posts_data() -> list[dict[str, Any]]:
    """Fetch posts data from JSONPlaceholder."""
    return await fetch_json(POSTS_DATA_URL)

