#!/usr/bin/env python
from fastapi import FastAPI

from routes.customers import customerRouter as customer_router
from routes.menu import menuRouter as menu_router
from routes.shops import shopRouter as shop_router
from routes.orders import orderRouter as order_router

app = FastAPI()

app.include_router(customer_router, tags=["customer"], prefix="/customer")
app.include_router(menu_router, tags=["menu"], prefix="/menu")
app.include_router(shop_router, tags=["shop"], prefix="/shop")
app.include_router(order_router, tags=["order"], prefix="/order")

@app.get("/")
async def root():
    return {"message": "welcome"}
