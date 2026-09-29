import io
import json
from typing import Optional

from app.config import settings

from app.models.schemas import (
    RecommendationResponse
)

from .catalog import fallback_items


SYSTEM = """
You are PocketSmart AI, a budget-conscious
lifestyle recommendation assistant.

Return useful and realistic recommendations.

Never claim that you verified live stock,
live inventory, or live prices.

Use the user's exact budget as a hard upper
limit for the combined recommended items.

Platform names are discovery targets and do
not prove inventory availability.

Estimated prices must be treated as estimates.

For jewelry images, use only visible outfit
style and color information.

Do not infer sensitive personal information
about the person in an image.

Return structured recommendation data.
"""


def _fallback(
    planner: str,
    budget: float,
    reason: str
) -> dict:

    if planner == "home":

        allocation = {
            "Furniture": round(
                budget * 0.45,
                2
            ),
            "Lighting": round(
                budget * 0.20,
                2
            ),
            "Decor": round(
                budget * 0.20,
                2
            ),
            "Buffer": round(
                budget * 0.15,
                2
            )
        }

    elif planner == "party":

        allocation = {
            "Food": round(
                budget * 0.50,
                2
            ),
            "Decoration": round(
                budget * 0.20,
                2
            ),
            "Venue": round(
                budget * 0.20,
                2
            ),
            "Buffer": round(
                budget * 0.10,
                2
            )
        }

    else:

        allocation = {
            "Main piece": round(
                budget * 0.50,
                2
            ),
            "Earrings": round(
                budget * 0.20,
                2
            ),
            "Bracelet": round(
                budget * 0.15,
                2
            ),
            "Buffer": round(
                budget * 0.15,
                2
            )
        }

    return {

        "planner": planner,

        "budget": budget,

        "budget_allocation": allocation,

        "summary": (
            "A local fallback plan was "
            f"generated because {reason}"
        ),

        "tips": [

            "Compare final prices before purchase.",

            "Keep a small buffer for delivery "
            "or last-minute costs.",

            "Treat marketplace prices as estimates "
            "until checked on the linked site."
        ],

        "recommendations": fallback_items(
            planner,
            budget
        ),

        "source": "fallback",

        "disclaimer": (
            "Demo recommendations use estimated "
            "prices and search links; they are not "
            "live inventory or price guarantees."
        )
    }


def _client():

    if not settings.GEMINI_API_KEY:
        return None

    try:

        from google import genai

        return genai.Client(
            api_key=settings.GEMINI_API_KEY
        )

    except ImportError:

        return None


def _prompt(
    planner: str,
    data: dict
) -> str:

    return f"""
Create a PocketSmart AI {planner}
budget plan.

User input:

{json.dumps(
    data,
    indent=2
)}

Requirements:

- Keep total estimated recommendation
  cost at or below the budget.

- Give 4-6 concrete recommendation ideas.

- Include platform.

- Include estimated price.

- Include category.

- Include a concise reason.

- Include a search URL for the platform.

- Allocate the budget across meaningful
  categories.

- Do not claim live availability.

- Do not claim that prices are live.

- Keep tips practical and concise.

Return only structured JSON.
"""


def generate(
    planner: str,
    data: dict,
    image_bytes: Optional[bytes] = None,
    mime_type: Optional[str] = None
) -> dict:

    client = _client()

    if not client:

        return _fallback(
            planner,
            float(data["budget"]),
            "no GEMINI_API_KEY is configured."
        )

    try:

        contents = [
            _prompt(
                planner,
                data
            )
        ]

        if image_bytes:

            from PIL import Image

            image = Image.open(
                io.BytesIO(image_bytes)
            ).convert("RGB")

            contents.append(image)

            contents.append(
                """
Also consider the visible outfit colors
and visible style in this image when
selecting jewelry.
"""
            )

        response = client.models.generate_content(

            model=settings.GEMINI_MODEL,

            contents=contents,

            config={
                "system_instruction": SYSTEM,

                "response_mime_type":
                    "application/json",

                "response_schema":
                    RecommendationResponse,

                "temperature": 0.4,

                "max_output_tokens": 2500
            }
        )

        parsed = (
            RecommendationResponse
            .model_validate_json(
                response.text
            )
        )

        result = parsed.model_dump()

        result["source"] = "gemini"

        return result

    except Exception as exc:

        return _fallback(
            planner,
            float(data["budget"]),
            (
                "the Gemini request was "
                f"unavailable "
                f"({type(exc).__name__})."
            )
        )