from pydantic import BaseModel
from typing import Optional
from decimal import Decimal
from pydantic import ConfigDict

#Schemas Order
class OrderModel(BaseModel):
    id: int
    items: list[OrderItemModel] = []

#Schemas OrderItem
class OrderItemModel(BaseModel):
    id: int
    order_id: int
    product_id: int
    quantity: int
    unit_price: Decimal
    notes: Optional[str]

    class Config:
        model_config = ConfigDict(from_attributes=True)

# Schemas de Categoria
class CategoryCreate(BaseModel):
    name: str
    description: Optional[str] = None

class CategoryResponse(CategoryCreate):
    id: int

# Schemas de Produto
class ProductCreate(BaseModel):
    name: str
    description: Optional[str] = None
    price: Decimal
    image_url: Optional[str] = None

class ProductResponse(ProductCreate):
    id: int
  