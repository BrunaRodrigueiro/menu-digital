# Rotas relacionadas aos pedidos dos clientes

from fastapi import APIRouter, status, HTTPException
from fastapi.encoders import jsonable_encoder

from models.models import Order, OrderItem, Product
from schemas.schemas import OrderItemModel, OrderCreate
from db.database import SessionLocal


orders_router = APIRouter(
    prefix="/orders",
    tags=['orders']
)

# Lista todos os pedido
@orders_router.get("/")
async def list_orders():
    with SessionLocal() as session:
        orders = session.query(Order).all()

        response = [
            {
                "id": order.id,
                "customer_name": order.customer_name,
                "general_notes": order.general_notes,
                "items": order.items
            }
            for order in orders
        ]

        return jsonable_encoder(response)

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
async def create_order(order_data: OrderCreate):
    session = SessionLocal()

    new_order = Order(
    customer_name=order_data.customer_name,
    general_notes=order_data.general_notes
)

    session.add(new_order)
    session.flush()

    for item in order_data.items:
        product = session.query(Product).filter(
            Product.id == item.product_id
        ).first()

        if not product:
            session.rollback()
            raise HTTPException(
                status_code=404,
                detail=f"Produto {item.product_id} não encontrado"
            )

        new_item = OrderItem(
            order_id=new_order.id,
            product_id=item.product_id,
            quantity=item.quantity,
            unit_price=product.price,
            notes=item.notes
        )

        session.add(new_item)

    session.commit()
    session.refresh(new_order)

    return {
        "id": new_order.id,
        "items": new_order.items
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

@orders_router.delete("/{order_id}")
async def delete_order(order_id: int):
    session = SessionLocal()

    order = session.query(Order).filter(
        Order.id == order_id
    ).first()

    if not order:
        raise HTTPException(
            status_code=404,
            detail="Pedido não encontrado"
        )

    session.query(OrderItem).filter(
        OrderItem.order_id == order_id
    ).delete()

    session.delete(order)
    session.commit()

    return {"message": "Pedido apagado com sucesso!"}