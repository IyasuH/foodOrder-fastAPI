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

from models.menu import MenuSchema, UpdateMenuModel
menuRouter = APIRouter()

@menuRouter.post("/", response_description="Menu data added into db", response_model=MenuSchema)
async def add_menu_data(menu: MenuSchema = Body(...)):
    menu = jsonable_encoder(menu)
    new_menu = await db["menus"].insert_one(menu)
    created_menu = await db["menus"].find_one({"mid": new_menu.inserted_id})
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_menu)

@menuRouter.get("/", response_description="List all menu", response_model=List[MenuSchema])
async def list_menu():
    menus = await db["menus"].find(limit=100).to_list(1000)
    return menus

@menuRouter.get("/{id}", response_description="Single menu by its id", response_model=MenuSchema)
async def find_menu(id: str):
    if (menu := await db['menus'].find_one({"mid": id})) is not None:
        return menu
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Menu with ID {id} not found")

@menuRouter.delete("/{id}", response_description="Delete menu")
async def delete_menu(id: str):
    delete_menu = await db["menus"].delete_one({"mid": id})
    if delete_menu.deleted_count == 1:
        return Response(status_code = status.HTTP_204_NO_CONTENT)
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Menu with ID {id} not found")

@menuRouter.put('/{id}', response_description="Update a menu", response_model=MenuSchema)
async def update_menu(id: str, menuU: UpdateMenuModel = Body(...)):
    menu_dict = {k: v for k, v in menuU.dict().items() if v is not None}
    if len(menu_dict) >= 1:
        update_menu = await db["menus"].update_one({"mid": id}, {"$set": menu_dict})
        if update_menu.modified_count==1:
            if (update_menu := await db["menus"].find_one({"mid": id})) is not None:
                return update_menu
    if (existing_menu := await db["menus"].find_one({"mid": id})) is not None:
        return existing_menu
    raise HTTPException(status_code=404, detail=f"menu {id} not found")
