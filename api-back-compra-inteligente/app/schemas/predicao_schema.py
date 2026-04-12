from pydantic import BaseModel, Field
from typing import Optional, List


class PredicaoSchema(BaseModel):
    age: int = Field(..., json_schema_extra={"example": 30})
    gender: str = Field(..., json_schema_extra={"example": "Male"})
    device_type: str = Field(..., json_schema_extra={"example": "Mobile"})
    previous_purchases: int = Field(..., json_schema_extra={"example": 1})
    discount_seen: int = Field(..., json_schema_extra={"example": 1})
    ad_clicked: int = Field(..., json_schema_extra={"example": 0})
    returning_user: int = Field(..., json_schema_extra={"example": 1})
    cart_items: int = Field(..., json_schema_extra={"example": 2})


class PredicaoResponseSchema(BaseModel):
    probabilidade_compra: float
    faixa_conversao: str