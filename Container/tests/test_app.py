from __future__ import annotations

from inspect import iscoroutinefunction

from app.main import app, health


def test_application_exists() -> None:
    """Check that the FastAPI application exists."""
    assert app.title == "Container Homework"


def test_health_is_async() -> None:
    """Check that the health endpoint is asynchronous."""
    assert iscoroutinefunction(health)


def test_health_route_exists() -> None:
    """Check that the health route is registered."""
    routes = {route.path for route in app.routes}

    assert "/health" in routes


def test_index_route_exists() -> None:
    """Check that the index route is registered."""
    routes = {route.path for route in app.routes}

    assert "/" in routes


def test_create_note_route_exists() -> None:
    """Check that the note creation route is registered."""
    routes = {
        (route.path, tuple(route.methods or []))
        for route in app.routes
    }

    assert ("/notes", ("POST",)) in routes