# Rotas relacionadas aos produtos do cardápio

from fastapi import APIRouter, HTTPException

from db.database import SessionLocal
from models.models import Product, Category, ProductCategory
from schemas.schemas import ProductCreate


products_router = APIRouter(
    prefix="/products",
    tags=["Products"]
)


@products_router.post("/")
async def create_product(product: ProductCreate):
    session = SessionLocal()

    category = session.query(Category).filter(
        Category.id == product.category_id
    ).first()

    if not category:
        raise HTTPException(
            status_code=404,
            detail="Categoria não encontrada"
        )

    new_product = Product(
        name=product.name,
        description=product.description,
        price=product.price,
        image_url=product.image_url
    )

    session.add(new_product)
    session.commit()
    session.refresh(new_product)

    product_category = ProductCategory(
        product_id=new_product.id,
        category_id=product.category_id
    )

    session.add(product_category)
    session.commit()

    return new_product


@products_router.get("/")
async def list_products():
    session = SessionLocal()

    products = session.query(Product).all()

    return products


@products_router.get("/{product_id}")
async def get_product(product_id: int):
    session = SessionLocal()

    product = session.query(Product).filter(
        Product.id == product_id
    ).first()

    if not product:
        raise HTTPException(
            status_code=404,
            detail="Produto não encontrado"
        )

    return product