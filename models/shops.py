#!/usr/bin/env python
import uuid
from typing import Optional

from pydantic import BaseModel, Field, EmailStr
class ShopsSchema(BaseModel):
    id: str=Field(default_factory=uuid.uuid4, alias="sid")
    name: str = Field(...)
    email: EmailStr = Field(...)
    addr: str = Field(...)
    desc: str = Field(...)
    class Config:
        schema_extra = {
                "example":{
                    "sid": "hid0f-fiu3h-fui3r",
                    "name": "Resturant Name",
                    "email":"resturant@mail.com",
                    "addr": "https://maps.app.goo.gl/hvdydtrs5e",
                    "desc": "description about the resturant"
                    }
                }

class UpdateShopModel(BaseModel):
    name: Optional[str]
    email: Optional[EmailStr]
    addr: Optional[str]
    desc: Optional[str]
    class Config:
        schema_extra = {
                "example": {
                    "name": "Resturant Name",
                    "email":"resturant@mail.com",
                    "addr": "https://maps.app.goo.gl/hvdydtrs5e",
                    "desc": "description about the resturant"
                    }
                }
