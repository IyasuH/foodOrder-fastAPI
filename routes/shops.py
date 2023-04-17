#!/usr/bin/env python
from fastapi import APIRouter, Body, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import Response, JSONResponse
import motor.motor_asyncio
import os, sys
from typing import List

mongoURL = os.environ.get("MongoURL")
mongoPassword = os.environ.get("MongoPassword")

mongoURL_P= mongoURL.replace('<password>', mongoPassword)

client = motor.motor_asyncio.AsyncIOMotorClient(mongoURL_P)
db = client.foodOrder

current = os.path.dirname(os.path.realpath(__file__))
parent_dir = os.path.dirname(current)

sys.path.append(parent_dir)


from models.shops import ShopsSchema, UpdateShopModel
shopRouter = APIRouter()

@shopRouter.post("/", response_description="shop data added into db", response_model=ShopsSchema)
async def add_shop_data(shop: ShopsSchema = Body(...)):
    shop = jsonable_encoder(shop)
    new_shop = await db["shops"].insert_one(shop)
    created_shop = await db["shops"].find_one({"sid": new_shop.inserted_id})
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_shop)

@shopRouter.get("/", response_description="List all orders", response_model=List[ShopsSchema])
async def list_shop():
    shops = await db["shops"].find(limit=100).to_list(1000)
    return shops

@shopRouter.get("/{id}", response_description="Single order by its id", response_model=ShopsSchema)
async def find_shop(id: str):
    if (shop := await db['shops'].find_one({"sid": id})) is not None:
        return shop
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"shop with ID {id} not found")

@shopRouter.delete("/{id}", response_description="Delete shop")
async def delete_shop(id: str):
    delete_shop = await db["shops"].delete_one({"sid": id})
    if delete_shop.deleted_count == 1:
        return Response(status_code = status.HTTP_204_NO_CONTENT)
    raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"shop with ID {id} not found")

@shopRouter.put('/{id}', response_description="Update a shop", response_model=ShopsSchema)
async def update_shop(id: str, shopU: UpdateShopModel = Body(...)):
    shop_dict = {k: v for k, v in shopU.dict().items() if v is not None}
    if len(shop_dict) >= 1:
        update_shop = await db["shops"].update_one({"sid": id}, {"$set": shop_dict})
        if update_shop.modified_count==1:
            if (update_shop := await db["shops"].find_one({"sid": id})) is not None:
                return update_shop
    if (existing_shop := await db["shops"].find_one({"sid": id})) is not None:
        return existing_shop
    raise HTTPException(status_code=404, detail=f"shop {id} not found")
