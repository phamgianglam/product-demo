from datetime import datetime, tzinfo
from typing import List, Any, Optional
from uuid import UUID, uuid4
from pydantic import BaseModel, Field, validator


class ProductPostModel(BaseModel):
    name: str = Field(..., description="name of product")
    description: str = Field(..., description="description of product")
    price: int = Field(..., description="price of product")
    date: Optional[datetime] = Field(
        datetime.now(), description="date that product is updated"
    )

    class Config:
        allow_population_by_field_name = True
        orm_mode = True
        extra = "forbid"
        schema_extra = {
            "example": {
                "name": "sample product",
                "description": "this is sample product",
                "price": 20,
                "date": "2022-01-01T13:40:40.603227",
            }
        }


class ProductModel(BaseModel):
    id_: UUID = Field(..., alias="id of product")
    name: str = Field(..., description="name of product")
    description: str = Field(..., description="description of product")
    price: int = Field(..., description="price of product")
    date: Optional[datetime] = Field(
        datetime.now(), description="date that product is updated"
    )

    class Config:
        allow_population_by_field_name = True
        orm_mode = True
        extra = "forbid"
        schema_extra = {
            "example": {
                "id": uuid4(),
                "name": "sample product",
                "description": "this is sample product",
                "price": 20,
                "date": "2022-01-01T13:40:40.603227",
            }
        }
