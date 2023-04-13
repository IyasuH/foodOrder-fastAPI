#!/usr/bin/env python
import uuid
from typing import Optional
from datetime import datetime

from pydantic import BaseModel, Field, EmailStr

class OrdersSchema(BaseModel):
    id: str=Field(default_factory=uuid.uuid4, alias="oid")
    cid: str = Field(...)#customerId
    mid: str = Field(...)#menuId
    orderTime: datetime = Field(...)
    status: bool = Field(...)
    ariveTime: datetime = Field(...)
    deliveryPlace: str = Field(...)
    revenuMade: float = Field(...)
    quantity: int = Field(...)
    class Config:
        schema_extra = {
                "example":{
                    "oid":"fgyf56-yfgv6-e4ersfcf",
                    "cid":"huyuv6-ctye5-cr74w",
                    "mid":"hvyft-rtd45-hf666",
                    "orderTime": datetime.now(),
                    "status": True,
                    "ariveTime": datetime.now(),
                    "deliveryPlace": "https://maps.app.goo.gl/hvdydtrs5e",
                    "revenuMade": 3436.45,
                    "quantity": 10
                    }
                }
class UpdateOrderModel(BaseModel):
    cid: Optional[str]#customerId
    mid: Optional[str]#menuId
    orderTime: Optional[datetime]
    status: Optional[str]
    ariveTime: Optional[datetime]
    deliveryPlace: Optional[str]
    revenuMade: Optional[float]
    quantity: Optional[int]
    class Config:
        schema_extra = {
                "example": {
                    "cid":"huyuv6-ctye5-cr74w",
                    "mid":"hvyft-rtd45-hf666",
                    "orderTime": datetime.now(),
                    "status": True,
                    "ariveTime": datetime.now(),
                    "deliveryPlace": "https://maps.app.goo.gl/hvdydtrs5e",
                    "revenuMade": 3436.45,
                    "quantity": 10                    
                    }
                }
