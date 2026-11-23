from sqlalchemy import Column, Integer, String, Float, ForeignKey
from database import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(String(255), nullable=True)
    price = Column(Float, nullable=False)
    image = Column(String(255), nullable=True)
    active = Column(Integer, default=1)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
