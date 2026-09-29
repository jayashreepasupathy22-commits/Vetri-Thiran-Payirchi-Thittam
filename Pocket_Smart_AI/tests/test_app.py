import os

os.environ["JWT_SECRET"] = (
    "test-secret-for-pocketsmart"
)

os.environ["DATABASE_URL"] = (
    "sqlite:///./data/test_pocketsmart.db"
)


from fastapi.testclient import TestClient

from app.main import app
from services.catalog import fallback_items


client = TestClient(app)


def test_health():

    response = client.get(
        "/api/health"
    )

    assert response.status_code == 200

    assert (
        response.json()["status"]
        == "ok"
    )


def test_testimonial_page():

    response = client.get("/testimonial")

    assert response.status_code == 200
    assert "Testimonials" in response.text


def test_home_fallback_without_gemini():

    response = client.post(
        "/api/generate-home",

        json={
            "budget": 20000,
            "room_type": "Living Room",
            "lights": 5,
            "fans": 4,
            "dining_tables": 0,
            "style": "Modern",
            "notes": ""
        }
    )


    assert response.status_code == 200


    data = response.json()


    assert data["planner"] == "home"


    assert data["budget"] == 20000


    assert (
        len(data["recommendations"])
        > 0
    )


def test_fallback_items_respect_budget():

    recommendations = fallback_items(
        "home",
        1000
    )

    assert recommendations == []


def test_register_login_session():

    email = (
        "test_pocketsmart@example.com"
    )


    register_response = client.post(
        "/api/register",

        json={
            "name": "Test User",
            "email": email,
            "password": "secret123"
        }
    )


    assert register_response.status_code in (
        200,
        409
    )


    login_response = client.post(
        "/api/login",

        json={
            "email": email,
            "password": "secret123"
        }
    )


    assert (
        login_response.status_code
        == 200
    )


    session_response = client.get(
        "/api/session-info"
    )


    assert (
        session_response.status_code
        == 200
    )


    assert (
        session_response
        .json()["authenticated"]
        is True
    )