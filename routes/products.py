from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models.product import Product
from models.category import Category

router = APIRouter(prefix="/products", tags=["Products"])


@router.post("/")
def create_product(
    name: str,
    price: float,
    category_id: int,
    description: str = None,
    image: str = None,
    db: Session = Depends(get_db)
):
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    product = Product(
        name=name,
        price=price,
        category_id=category_id,
        description=description,
        image=image
    )
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


@router.get("/")
def list_products(db: Session = Depends(get_db)):
    return db.query(Product).all()


@router.get("/{product_id}")
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.put("/{product_id}")
def update_product(
    product_id: int,
    name: str = None,
    price: float = None,
    category_id: int = None,
    description: str = None,
    image: str = None,
    active: int = None,
    db: Session = Depends(get_db)
):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    if category_id is not None:
        category = db.query(Category).filter(Category.id == category_id).first()
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")
        product.category_id = category_id

    if name is not None:
        product.name = name
    if price is not None:
        product.price = price
    if description is not None:
        product.description = description
    if image is not None:
        product.image = image
    if active is not None:
        product.active = active

    db.commit()
    db.refresh(product)
    return product


@router.delete("/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    db.delete(product)
    db.commit()
    return {"message": "Product deleted"}
