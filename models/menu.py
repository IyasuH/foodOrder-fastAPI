#!/usr/bin/env python
from typing import Optional
import uuid
from datetime import datetime

from pydantic import BaseModel, Field, EmailStr

class MenuSchema(BaseModel):
    id: str=Field(default_factory=uuid.uuid4, alias="mid")
    sid: str = Field(...)
    itemName: str = Field(...)
    itemPrice: float = Field(...)
    quantity: int = Field(...)
    class Config:
        schema_extra = {
                "example": {
                    "mid": "d3yy2o-e3uyr-4r4f3",
                    "sid": "r43rfc1-f1g861g-1fg18g",
                    "itemName": "item name",
                    "itemPrice": 2343.5,
                    "quantity": 20
                    }
                }
class UpdateMenuModel(BaseModel):
    sid: Optional[str]
    itemName: Optional[str]
    itemPrice: Optional[float]
    quantity: Optional[int]
    class Config:
        schema_extra = {
                "example": {
                    "sid": "r43rfc1-f1g861g-1fg18g",
                    "itemName": "item name",
                    "itemPrice": 2343.5,
                    "quantity": 20                    
                    }
                }
