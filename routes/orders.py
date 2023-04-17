
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

from models.orders import OrdersSchema, UpdateOrderModel
orderRouter = APIRouter()

@orderRouter.post("/", response_description="Order data added into db", response_model=OrdersSchema)
async def add_order_data(order: OrdersSchema = Body(...)):
    order = jsonable_encoder(order)
    new_order = await db["orders"].insert_one(order)
    created_order = await db["orders"].find_one({"oid": new_order.inserted_id})
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_order)

@orderRouter.get("/", response_description="List all orders", response_model=List[OrdersSchema])
async def list_order():
    orders = await db["orders"].find(limit=100).to_list(1000)
    return orders

@orderRouter.get("/{id}", response_description="Single order by its id", response_model=OrdersSchema)
async def find_order(id: str):
    if (order := await db['orders'].find_one({"oid": id})) is not None:
        return order
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Order with ID {id} not found")

@orderRouter.delete("/{id}", response_description="Delete order")
async def delete_order(id: str):
    delete_order = await db["orders"].delete_one({"oid": id})
    if delete_order.deleted_count == 1:
        return Response(status_code = status.HTTP_204_NO_CONTENT)
    raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail=f"Order with ID {id} not found")

@orderRouter.put('/{id}', response_description="Update a order", response_model=OrdersSchema)
async def update_order(id: str, orderU: UpdateOrderModel = Body(...)):
    order_dict = {k: v for k, v in orderU.dict().items() if v is not None}
    if len(order_dict) >= 1:
        update_order = await db["orders"].update_one({"oid": id}, {"$set": order_dict})
        if update_order.modified_count==1:
            if (update_order := await db["orders"].find_one({"oid": id})) is not None:
                return update_order
    if (existing_order := await db["orders"].find_one({"oid": id})) is not None:
        return existing_order
    raise HTTPException(status_code=404, detail=f"order {id} not found")
