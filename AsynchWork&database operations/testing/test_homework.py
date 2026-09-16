import inspect

from jsonplaceholder_requests import (
    fetch_json,
    fetch_posts_data,
    fetch_users_data,
)
from models import Base, Post, User


def test_fetch_functions_are_async() -> None:
    """Check that HTTP functions are asynchronous."""
    assert inspect.iscoroutinefunction(fetch_json)
    assert inspect.iscoroutinefunction(fetch_users_data)
    assert inspect.iscoroutinefunction(fetch_posts_data)


def test_models_are_registered() -> None:
    """Check that User and Post models are registered in SQLAlchemy metadata."""
    assert User.__tablename__ == "users"
    assert Post.__tablename__ == "posts"

    mapped_classes = {
        mapper.class_
        for mapper in Base.registry.mappers
    }

    assert User in mapped_classes
    assert Post in mapped_classes


def test_user_model_fields() -> None:
    """Check required User model fields."""
    columns = User.__table__.columns

    assert "id" in columns
    assert "name" in columns
    assert "username" in columns
    assert "email" in columns


def test_post_model_fields() -> None:
    """Check required Post model fields."""
    columns = Post.__table__.columns

    assert "id" in columns
    assert "user_id" in columns
    assert "title" in columns
    assert "body" in columns


def test_user_post_relationships() -> None:
    """Check User.posts and Post.user relationships."""
    user_relationship = User.__mapper__.relationships["posts"]
    post_relationship = Post.__mapper__.relationships["user"]

    assert user_relationship.back_populates == "user"
    assert post_relationship.back_populates == "posts"


def test_post_user_foreign_key() -> None:
    """Check that Post.user_id references users.id."""
    foreign_keys = Post.__table__.c.user_id.foreign_keys

    assert len(foreign_keys) == 1

    foreign_key = next(iter(foreign_keys))

    assert str(foreign_key.target_fullname) == "users.id"