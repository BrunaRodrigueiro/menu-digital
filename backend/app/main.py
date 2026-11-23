from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from db.database import Base, engine
from models import models

from routes.categories import categories_router
from routes.orders import orders_router
from routes.products import products_router

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

# Rotas separadas na aplicação
app.include_router(categories_router)
app.include_router(orders_router)
app.include_router(products_router)