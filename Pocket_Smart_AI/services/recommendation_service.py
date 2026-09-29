from .gemini_utils import generate

from app.models.schemas import (
    HomeRequest,
    PartyRequest,
    JewelryRequest
)


def home(
    data: HomeRequest
):

    return generate(
        "home",
        data.model_dump()
    )


def party(
    data: PartyRequest
):

    return generate(
        "party",
        data.model_dump()
    )


def jewelry(
    data: JewelryRequest,
    image_bytes=None,
    mime_type=None
):

    return generate(
        "jewelry",
        data.model_dump(),
        image_bytes=image_bytes,
        mime_type=mime_type
    )