from pydantic import BaseModel
from typing import Optional
from decimal import Decimal
from pydantic import ConfigDict

# Schema para CRIAR item
class OrderItemCreate(BaseModel):
    product_id: int
    quantity: int
    notes: Optional[str] = None

# Schema para CRIAR pedido
class OrderCreate(BaseModel):
    customer_name: Optional[str] = None
    general_notes: Optional[str] = None
    items: list[OrderItemCreate]

# Schema OrderItem
class OrderItemModel(BaseModel):
    id: int
    order_id: int
    product_id: int
    quantity: int
    unit_price: Decimal
    notes: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

# Schema Order
class OrderModel(BaseModel):
    id: int
    items: list[OrderItemModel] = []

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
    category_id: int

class ProductResponse(ProductCreate):
    id: int
  