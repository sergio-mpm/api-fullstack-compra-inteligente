from pydantic import BaseModel, Field
from typing import Optional, List


class PredicaoSchema(BaseModel):
    age: int = Field(..., example=30)
    gender: str = Field(..., example="Male")
    device_type: str = Field(..., example="Mobile")
    time_on_site: float = Field(..., example=18.5)
    pages_viewed: int = Field(..., example=6)
    previous_purchases: int = Field(..., example=1)
    cart_items: int = Field(..., example=2)
    discount_seen: int = Field(..., example=1)
    ad_clicked: int = Field(..., example=0)
    returning_user: int = Field(..., example=1)
    avg_session_time: float = Field(..., example=12.0)
    bounce_rate: float = Field(..., example=30.0)


class PredicaoResponseSchema(BaseModel):
    prediction: int
    probability: float
    label: str