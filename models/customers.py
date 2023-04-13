#!/usr/bin/env python
from typing import Optional
import uuid
from pydantic import BaseModel, Field, EmailStr

class CustomerSchema(BaseModel):
    id: str=Field(default_factory=uuid.uuid4,alias="cid")
    fullName: str = Field(...)
    email: EmailStr = Field(...)

    class Config:
        schema_extra = {
                "example": {
                    "cid": "ckjbufgp482",
                    "fullName": "Iyasu H",
                    "email": "eyasu@mail.com"
                    }
                }

class UpdateCustomerModel(BaseModel):
    fullName: Optional[str]
    email: Optional[EmailStr]
    class Config: 
        schema_extra = {
                "example": {
                    "fullName": "iyasu h",
                    "email": "iyasu@mail.com"
                    }
                }
