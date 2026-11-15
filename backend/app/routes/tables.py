# Rotas relacionadas às mesas do estabelecimento

from fastapi import APIRouter

tables_router=APIRouter()

@tables_router.get('/')
async def hello():
    return{"message: Hello World"}