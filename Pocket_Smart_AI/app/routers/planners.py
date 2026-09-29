import json

from fastapi import (
    APIRouter,
    File,
    Form,
    HTTPException,
    Request,
    UploadFile
)

from ..auth import get_current_user_id

from ..config import settings

from ..database import get_db

from ..models.schemas import (
    HomeRequest,
    PartyRequest,
    JewelryRequest
)

from services.recommendation_service import (
    home,
    party,
    jewelry
)


router = APIRouter(
    prefix="/api"
)


def save_history(
    request: Request,
    planner: str,
    payload: dict,
    result: dict
):

    user_id = get_current_user_id(
        request
    )

    if not user_id:
        return

    with get_db() as db:

        db.execute(
            """
            INSERT INTO recommendations
            (
                user_id,
                planner,
                input_json,
                result_json
            )
            VALUES (?, ?, ?, ?)
            """,
            (
                user_id,
                planner,
                json.dumps(payload),
                json.dumps(result)
            )
        )


@router.post("/generate-home")
def generate_home(
    payload: HomeRequest,
    request: Request
):

    result = home(payload)

    save_history(
        request,
        "home",
        payload.model_dump(),
        result
    )

    return result


@router.post("/generate-party")
def generate_party(
    payload: PartyRequest,
    request: Request
):

    result = party(payload)

    save_history(
        request,
        "party",
        payload.model_dump(),
        result
    )

    return result


@router.post("/generate-jewelry")
async def generate_jewelry(
    request: Request,

    budget: float = Form(...),

    occasion: str = Form(...),

    style: str = Form(
        "Elegant"
    ),

    outfit_color: str = Form(
        "Not specified"
    ),

    notes: str = Form(
        ""
    ),

    outfit_image: UploadFile | None = File(
        None
    )
):

    payload = JewelryRequest(
        budget=budget,
        occasion=occasion,
        style=style,
        outfit_color=outfit_color,
        notes=notes
    )

    image_bytes = None

    mime_type = None

    if outfit_image:

        allowed_types = {
            "image/jpeg",
            "image/png",
            "image/webp"
        }

        if outfit_image.content_type not in allowed_types:

            raise HTTPException(
                status_code=400,
                detail=(
                    "Only JPEG, PNG, or WEBP "
                    "images are supported."
                )
            )

        image_bytes = (
            await outfit_image.read()
        )

        if len(image_bytes) > settings.MAX_IMAGE_BYTES:

            raise HTTPException(
                status_code=413,
                detail=(
                    "Image must be "
                    "5 MB or smaller."
                )
            )

        mime_type = (
            outfit_image.content_type
        )

    result = jewelry(
        payload,
        image_bytes,
        mime_type
    )

    save_history(
        request,
        "jewelry",
        payload.model_dump(),
        result
    )

    return result


@router.post(
    "/recommendations-details"
)
def recommendation_details(
    payload: dict
):

    planner = payload.get(
        "planner"
    )

    if planner not in {
        "home",
        "party",
        "jewelry"
    }:

        raise HTTPException(
            status_code=400,
            detail=(
                "planner must be "
                "home, party, or jewelry"
            )
        )

    return {
        "message": (
            "Use the planner endpoint "
            "for a fresh recommendation."
        ),
        "planner": planner
    }


@router.get("/history")
def history(
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

        rows = db.execute(
            """
            SELECT
                id,
                planner,
                input_json,
                result_json,
                created_at
            FROM recommendations
            WHERE user_id = ?
            ORDER BY id DESC
            LIMIT 50
            """,
            (user_id,)
        ).fetchall()

    return [
        {
            "id": row["id"],
            "planner": row["planner"],
            "input": json.loads(
                row["input_json"]
            ),
            "result": json.loads(
                row["result_json"]
            ),
            "created_at": row["created_at"]
        }
        for row in rows
    ]