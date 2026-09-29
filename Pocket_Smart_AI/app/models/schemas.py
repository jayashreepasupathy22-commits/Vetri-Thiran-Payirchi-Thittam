from typing import Literal

from pydantic import (
    BaseModel,
    Field,
    ConfigDict
)


Planner = Literal[
    "home",
    "party",
    "jewelry"
]


class RegisterRequest(BaseModel):

    name: str = Field(
        min_length=2,
        max_length=80
    )

    email: str = Field(
        min_length=5,
        max_length=160
    )

    password: str = Field(
        min_length=6,
        max_length=128
    )


class LoginRequest(BaseModel):

    email: str

    password: str


class HomeRequest(BaseModel):

    budget: float = Field(
        gt=0,
        le=10_000_000
    )

    room_type: str = Field(
        min_length=2,
        max_length=80
    )

    lights: int = Field(
        default=1,
        ge=0,
        le=100
    )

    fans: int = Field(
        default=0,
        ge=0,
        le=100
    )

    dining_tables: int = Field(
        default=0,
        ge=0,
        le=20
    )

    style: str = Field(
        default="Modern",
        max_length=80
    )

    notes: str = Field(
        default="",
        max_length=500
    )


class PartyRequest(BaseModel):

    budget: float = Field(
        gt=0,
        le=10_000_000
    )

    guests: int = Field(
        gt=0,
        le=10_000
    )

    event_type: str = Field(
        min_length=2,
        max_length=80
    )

    venue: str = Field(
        default="Flexible",
        max_length=120
    )

    food_preference: str = Field(
        default="Mixed",
        max_length=80
    )

    notes: str = Field(
        default="",
        max_length=500
    )


class JewelryRequest(BaseModel):

    budget: float = Field(
        gt=0,
        le=10_000_000
    )

    occasion: str = Field(
        min_length=2,
        max_length=80
    )

    style: str = Field(
        default="Elegant",
        max_length=80
    )

    outfit_color: str = Field(
        default="Not specified",
        max_length=80
    )

    notes: str = Field(
        default="",
        max_length=500
    )


class RecommendationItem(BaseModel):

    name: str

    category: str

    platform: str

    estimated_price: float = Field(
        ge=0
    )

    reason: str

    search_url: str


class RecommendationResponse(BaseModel):

    model_config = ConfigDict(
        extra="ignore"
    )

    planner: Planner

    budget: float

    budget_allocation: dict[str, float]

    summary: str

    tips: list[str]

    recommendations: list[
        RecommendationItem
    ]

    source: Literal[
        "gemini",
        "fallback"
    ]

    disclaimer: str