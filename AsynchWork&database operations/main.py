from __future__ import annotations

import asyncio
from typing import Any

from jsonplaceholder_requests import fetch_posts_data, fetch_users_data
from models import Base, Post, Session, User, engine


async def create_tables() -> None:
    """Create database tables."""
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)


async def add_users(users_data: list[dict[str, Any]]) -> None:
    """Add users to the database in a single batch."""
    users = [
        User(
            id=user_data["id"],
            name=user_data["name"],
            username=user_data["username"],
            email=user_data["email"],
        )
        for user_data in users_data
    ]

    async with Session() as session:
        session.add_all(users)
        await session.commit()


async def add_posts(posts_data: list[dict[str, Any]]) -> None:
    """Add posts to the database in a single batch."""
    posts = [
        Post(
            id=post_data["id"],
            user_id=post_data["userId"],
            title=post_data["title"],
            body=post_data["body"],
        )
        for post_data in posts_data
    ]

    async with Session() as session:
        session.add_all(posts)
        await session.commit()


async def async_main() -> None:
    """Run the complete asynchronous application cycle."""
    try:
        await create_tables()

        users_data, posts_data = await asyncio.gather(
            fetch_users_data(),
            fetch_posts_data(),
        )

        await add_users(users_data)
        await add_posts(posts_data)
    finally:
        await engine.dispose()


def main() -> None:
    """Run the asynchronous application."""
    asyncio.run(async_main())


if __name__ == "__main__":
    main()

