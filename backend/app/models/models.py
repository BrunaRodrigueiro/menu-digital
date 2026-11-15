from db.database import Base
from sqlalchemy import Column, Integer, Numeric, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

# Categoria
class Category(Base):
    __tablename__ = "category"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    description = Column(String(255))

    # Facilita a identificação do objeto durante o debug
    def __repr__(self):
        return f"<Category(id={self.id}, name='{self.name}')>"


# Categoria do Produto
class ProductCategory(Base):
    __tablename__ = "product_category"
    product_id = Column(Integer, ForeignKey("product.id"), primary_key=True)
    category_id = Column(Integer, ForeignKey("category.id"), primary_key=True)


# Produtos que contém no cardápio
class Product(Base):
    __tablename__ = "product"
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    description = Column(String(255))
    price = Column(Numeric(10, 2), nullable=False)
    image_url = Column(String(500), nullable=True)

    def __repr__(self):
        return f"<Product {self.name}>"

    order_items = relationship("OrderItem", back_populates="product")


# Comanda
class Order(Base):
    __tablename__ = "order"
    id = Column(Integer, primary_key=True)
    items = relationship("OrderItem", back_populates="order")

    def __repr__(self):
        return f"<Order {self.id}>"


# Representará os produtos vinculados a um pedido
class OrderItem(Base):
    __tablename__ = "order_item"
    id = Column(Integer, primary_key=True)
    order_id = Column( Integer, ForeignKey("order.id"))
    product_id = Column(Integer, ForeignKey("product.id"))
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Numeric(10, 2), nullable=False)
    notes = Column(String(500), nullable=True)
    order = relationship("Order", back_populates="items")
    product = relationship("Product", back_populates="order_items")

# Mesa do estabelecimento
# class Table(Base):
#     __tablename__='table'
#     id = Column(Integer, primary_key=True)
#     number = Column(Integer, nullable=False)
#     active = Column(Boolean, nullable=False)

#     orders = relationship('Order', back_populates='table')