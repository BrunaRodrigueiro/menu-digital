# Rotas relacionadas às categorias dos produtos (bebidas, lanches, sobremesas...)

from fastapi import APIRouter, HTTPException

from db.database import SessionLocal
from models.models import Category, ProductCategory
from schemas.schemas import CategoryCreate


categories_router = APIRouter(
    prefix="/categories",
    tags=["Categories"]
)


@categories_router.post("/")
async def create_category(category: CategoryCreate):
    session = SessionLocal()

    new_category = Category(
        name=category.name,
        description=category.description
    )

    session.add(new_category)
    session.commit()
    session.refresh(new_category)

    return new_category


@categories_router.get("/")
async def list_categories():
    session = SessionLocal()

    categories = session.query(Category).all()

    return categories


@categories_router.get("/{category_id}")
async def get_category(category_id: int):
    session = SessionLocal()

    category = session.query(Category).filter(
        Category.id == category_id
    ).first()

    if not category:
        raise HTTPException(
            status_code=404,
            detail="Categoria não encontrada"
        )

    return category

@categories_router.delete("/{category_id}")
async def delete_category(category_id: int):
    session = SessionLocal()

    category = session.query(Category).filter(
        Category.id == category_id
    ).first()

    if not category:
        raise HTTPException(
            status_code=404,
            detail="Categoria não encontrada"
        )

    session.query(ProductCategory).filter(
        ProductCategory.category_id == category_id
    ).delete()

    session.delete(category)
    session.commit()

    return {"message": "Categoria deletada com sucesso"}