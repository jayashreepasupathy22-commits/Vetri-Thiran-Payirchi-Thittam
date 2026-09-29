import sqlite3

from fastapi import (
    APIRouter,
    HTTPException,
    Request,
    Response
)

from ..auth import (
    hash_password,
    verify_password,
    create_token,
    COOKIE_NAME,
    get_current_user_id
)

from ..database import get_db

from ..models.schemas import (
    RegisterRequest,
    LoginRequest
)

from ..config import settings


router = APIRouter(
    prefix="/api"
)


@router.post("/register")
def register(
    payload: RegisterRequest,
    response: Response
):

    email = payload.email.strip().lower()

    name = payload.name.strip()

    password_hash = hash_password(
        payload.password
    )

    with get_db() as db:

        try:

            cursor = db.execute(
                """
                INSERT INTO users
                (
                    name,
                    email,
                    password_hash
                )
                VALUES (?, ?, ?)
                """,
                (
                    name,
                    email,
                    password_hash
                )
            )

            user_id = cursor.lastrowid

        except sqlite3.IntegrityError:

            raise HTTPException(
                status_code=409,
                detail=(
                    "An account with this "
                    "email already exists."
                )
            )

    token = create_token(user_id)

    response.set_cookie(
        COOKIE_NAME,
        token,
        httponly=True,
        samesite="lax",
        secure=settings.COOKIE_SECURE,
        max_age=60 * 60 * 24 * 7
    )

    return {
        "message": "Registration successful",
        "user": {
            "id": user_id,
            "name": name,
            "email": email
        }
    }


@router.post("/login")
def login(
    payload: LoginRequest,
    response: Response
):

    email = payload.email.strip().lower()

    with get_db() as db:

        user = db.execute(
            """
            SELECT *
            FROM users
            WHERE email = ?
            """,
            (email,)
        ).fetchone()

    if (
        not user
        or not verify_password(
            payload.password,
            user["password_hash"]
        )
    ):

        raise HTTPException(
            status_code=401,
            detail="Invalid email or password."
        )

    token = create_token(
        user["id"]
    )

    response.set_cookie(
        COOKIE_NAME,
        token,
        httponly=True,
        samesite="lax",
        secure=settings.COOKIE_SECURE,
        max_age=60 * 60 * 24 * 7
    )

    return {
        "message": "Login successful",
        "user": {
            "id": user["id"],
            "name": user["name"],
            "email": user["email"]
        }
    }


@router.post("/logout")
def logout(response: Response):

    response.delete_cookie(
        COOKIE_NAME
    )

    return {
        "message": "Logged out"
    }


@router.get("/session-info")
def session_info(
    request: Request
):

    user_id = get_current_user_id(
        request
    )

    if not user_id:

        return {
            "authenticated": False,
            "user": None
        }

    with get_db() as db:

        user = db.execute(
            """
            SELECT
                id,
                name,
                email,
                created_at
            FROM users
            WHERE id = ?
            """,
            (user_id,)
        ).fetchone()

    if not user:

        return {
            "authenticated": False,
            "user": None
        }

    return {
        "authenticated": True,
        "user": dict(user)
    }


@router.get("/session-data")
def session_data(
    request: Request
):

    user_id = get_current_user_id(
        request
    )

    if not user_id:

        raise HTTPException(
            status_code=401,
            detail="Login required"
        )

    with get_db() as db:

        row = db.execute(
            """
            SELECT COUNT(*) AS count
            FROM recommendations
            WHERE user_id = ?
            """,
            (user_id,)
        ).fetchone()

    return {
        "recommendation_count": row["count"]
    }