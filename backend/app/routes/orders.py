# Rotas relacionadas aos pedidos dos clientes

from fastapi import APIRouter, status, HTTPException
from fastapi.encoders import jsonable_encoder

from models.models import Order, OrderItem
from schemas.schemas import OrderItemModel
from db.database import SessionLocal


orders_router = APIRouter(
    prefix="/orders",
    tags=['orders']
)

# Lista todos os pedido
@orders_router.get('/')
async def list_orders():
    session = SessionLocal()

    orders = session.query(Order).all()

    return jsonable_encoder(orders)

# Lista os pedidos por ID
@orders_router.get('/{order_id}')
async def list_order_by_id(order_id: int):
    session = SessionLocal()

    order = session.query(Order).filter(Order.id == order_id).first()

    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Pedido não encontrado"
        )

    response = {
        "id": order.id,
        "items": order.items
    }

    return jsonable_encoder(response)


# Cria uma nova comanda/pedido e retorna o ID gerado
@orders_router.post("/", status_code=status.HTTP_201_CREATED)
async def create_order():
    session = SessionLocal()

    new_order = Order()

    session.add(new_order)
    session.commit()
    session.refresh(new_order)

    return {
        "id": new_order.id
    }
    
# Adiciona um produto a uma comanda/pedido já existente
@orders_router.post("/orders/", status_code=status.HTTP_201_CREATED)
async def add_item_to_order(order: OrderItemModel):
    session = SessionLocal()

    new_order_item = OrderItem(
        order_id=order.order_id,
        product_id=order.product_id,
        quantity=order.quantity,
        unit_price=order.unit_price,
        notes=order.notes
    )

    session.add(new_order_item)

    session.commit()
    
    session.refresh(new_order_item)

    response = {
    "id": new_order_item.id,
    "order_id": new_order_item.order_id,
    "product_id": new_order_item.product_id,
    "quantity": new_order_item.quantity,
    "unit_price": new_order_item.unit_price,
    "notes": new_order_item.notes
    }

    return jsonable_encoder(response)
