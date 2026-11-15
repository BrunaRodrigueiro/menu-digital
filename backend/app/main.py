from fastapi import FastAPI

from db.database import Base, engine
from models import models

from routes.categories import categories_router
from routes.orders import orders_router
from routes.products import products_router
from routes.tables import tables_router


app = FastAPI()

Base.metadata.create_all(bind=engine)

# Rotas separadas na aplicação
app.include_router(categories_router)
app.include_router(orders_router)
app.include_router(products_router)
app.include_router(tables_router)