# Rotas relacionadas às categorias dos produtos (bebidas, lanches, sobremesas...)

from fastapi import APIRouter

categories_router=APIRouter()

@categories_router.get('/')
async def hello():
    return{"message: Hello World"}