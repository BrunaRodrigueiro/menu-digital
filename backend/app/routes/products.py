# Rotas relacionadas aos produtos do cardápio

from fastapi import APIRouter

products_router=APIRouter()

@products_router.get('/')
async def hello():
    return{"message: Hello World"}