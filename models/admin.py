#!/usr/bin/env python
from typing import Optional
import uuid
from pydantic import BaseModel, Field, EmailStr

class AdminSchema(BaseModel):
    id: str=Field(default_factory=uuid.uuid4, alias="aid")
    fullName: str = Field(...)
    email: EmailStr = Field(...)
    password: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "aid": "ns3ugeyu-e3fr6f37r2f-briu37fr",
                "fullName": "Admin",
                "email": "admin@mail.com",
                "password": "hashedPassword"
            }
        }

class AdminLoginSchema(BaseModel):
    id: str = Field(alias="aid")
    email: EmailStr = Field(...)
    password: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "email": "admin@mail.com",
                "password": "hashedPassword"
            }
        }