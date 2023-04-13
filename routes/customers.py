#!/usr/bin/env python
from fastapi import APIRouter, Body, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import Response, JSONResponse
import motor.motor_asyncio
import os, sys
from typing import List

mongoURL = os.environ.get("mongoURL")
mongoPassword = os.environ.get("mongoPassword")

mongoURL_P= mongoURL.replace('<password>', mongoPassword)

client = motor.motor_asyncio.AsyncIOMotorClient(mongoURL_P)
db = client.foodOrder

current = os.path.dirname(os.path.realpath(__file__))
parent_dir = os.path.dirname(current)

sys.path.append(parent_dir)

from models.customers import CustomerSchema, UpdateCustomerModel
customerRouter = APIRouter()

@customerRouter.post("/", response_description="Customer data added into db", response_model=CustomerSchema)
async def add_customer_data(customer: CustomerSchema = Body(...)):
    customer = jsonable_encoder(customer)
    new_customer = await db['customers'].insert_one(customer)
    created_customer = await db['customers'].find_one({"cid": new_customer.inserted_id})
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_customer)
    # return created_customer
    #new_customer = await add_customer(customer)
    #return 

@customerRouter.get("/", response_description="List all customers", response_model=List[CustomerSchema])
async def list_customers():
    customers = await db["customers"].find(limit=100).to_list(1000)
    return customers

@customerRouter.get("/{id}", response_description="Single customer by its id", response_model=CustomerSchema)
async def find_customer(id: str):
    if (customer := await db['customers'].find_one({"cid": id})) is not None:
        return customer
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Customer with ID {id} not found")

@customerRouter.delete("/{id}", response_description="Delete customer")
async def delete_customer(id: str):
    delete_customer = await db["customers"].delete_one({"cid": id})
    if delete_customer.deleted_count == 1:
        return Response(status_code = status.HTTP_204_NO_CONTENT)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Customer with ID {id} not found")

@customerRouter.put('/{id}', response_description="Update a customer", response_model=CustomerSchema)
async def update_customer(id: str, customerU: UpdateCustomerModel = Body(...)):
    cust_dict = {k: v for k, v in customerU.dict().items() if v is not None}
    # customer = await db['customers'].find_one({"cid": id})
    if len(cust_dict) >= 1:
        update_customer = await db["customers"].update_one({"cid": id}, {"$set": cust_dict})
        if update_customer.modified_count==1:
            if (update_customer := await db["customers"].find_one({"cid": id})) is not None:
                return update_customer
    if (existing_customer := await db["customers"].find_one({"cid": id})) is not None:
        return existing_customer
    raise HTTPException(status_code=404, detail=f"student {id} not found")
