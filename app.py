#!/usr/bin/env python
from fastapi import FastAPI, Body, HTTPException, Depends, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse, Response
from typing import List

import motor.motor_asyncio

from routes.customers import customerRouter as customer_router
from routes.menu import menuRouter as menu_router
from routes.shops import shopRouter as shop_router
from routes.orders import orderRouter as order_router

from models.admin import AdminSchema, AdminLoginSchema
from auth.auth_handler import signJWT, get_password_hashed, verify_password
from auth.auth_bearer import JWTBearer

import os

mongoURL = os.environ.get("MongoURL")
mongoPassword = os.environ.get("MongoPassword")

mongoURL_P= mongoURL.replace('<password>', mongoPassword)

client = motor.motor_asyncio.AsyncIOMotorClient(mongoURL_P)
db = client.foodOrder


app = FastAPI()

app.include_router(customer_router, tags=["customer"], prefix="/customer")
app.include_router(menu_router, tags=["menu"], prefix="/menu")
app.include_router(shop_router, tags=["shop"], prefix="/shop")
app.include_router(order_router, tags=["order"], prefix="/order")

@app.get("/")
async def root():
    return {"message": "welcome"}

# this should be protected route
@app.post("/admin/signup", tags=["admin"])
async def create_admin(data: AdminSchema = Body(...)):
    # admin = db.get(data.email, None)
    admin = await db["admins"].find_one({"email":data.email})
    if admin is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Admin with this email addr already exits"
            )
    admin = {
     "fullName": data.fullName,
     "email": data.email,
     "password": get_password_hashed(data.password),
    }
    admin = jsonable_encoder(admin)
    new_admin = await db['admins'].insert_one(admin)
    # created_admin = await db['admins'].find_one({"aid": new_admin.inserted_id})
    return signJWT(new_admin.inserted_id)
    # return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_admin)
    # admin.append()

# async def check_admin(data: AdminLoginSchema):    
#     admins = await db["admins"].find().to_list()
#     for admin in admins:
#         # here when checking for password I should check for hashed one
#         if admin.email == data.email and admin.password == data.password:
#             # This means given email and password is correct
#             return True
#     return False

@app.post("/admin/login", tags=["admin"])
async def admin_login(data: AdminLoginSchema=Body(...)):
    # admin = db.get(data.email, None)
    admin = await db['admins'].find_one({"email":data.email})
    if admin is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect Email or password"
        )
    hashed_password = admin["password"]
    if not verify_password(data.password, hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect Password or email"
        )
    # if check_admin(data):
    return signJWT(data.aid)
    # return {"error": "wrong login detail"}

@app.delete("/admin/{id}", response_description="Delete admin", tags=["admin"])
async def delete_admin(id: str):
    delete_admin = await db["admins"].delete_one({"aid": id})
    if delete_admin.deleted_count == 1:
        return Response(status_code = status.HTTP_204_NO_CONTENT)
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Admin not found")

@app.get("/admin", response_description="List all customers", response_model=List[AdminSchema], tags=["admin"])
async def list_admin():
    admins = await db["admins"].find().to_list(1000)
    return admins

@app.get("/auth", dependencies=[Depends(JWTBearer())], tags=["posts"])
async def auth():
    return {"message": "authenticated"}