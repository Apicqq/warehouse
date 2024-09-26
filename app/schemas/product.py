from typing import Annotated, Optional

from pydantic import BaseModel, PositiveInt, NonNegativeInt, Field, ConfigDict


class ProductBase(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = Field(None, min_length=1, max_length=255)
    price: Optional[PositiveInt]
    amount_available: Optional[NonNegativeInt]


class ProductCreate(ProductBase):
    name: Annotated[str, Field(..., min_length=1, max_length=255)]
    description: Annotated[str, Field(..., min_length=1, max_length=255)]
    price: PositiveInt
    amount_available: NonNegativeInt


class ProductUpdate(ProductBase):
    pass


class ProductDB(ProductBase):
    id: int
    name: str
    description: str
    price: PositiveInt
    amount_available: NonNegativeInt
    model_config = ConfigDict(from_attributes=True)
