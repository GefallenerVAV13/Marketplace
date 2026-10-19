from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base
from app.models.product import Product

class Category(Base):
    __tablename__ = "categories"

    id:Mapped[int] = mapped_column(primary_key=True, index=True)
    name:Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    parent_id:Mapped[int | None] = mapped_column(ForeignKey("categories.id"), nullable=True)

    parent = relationship("Category", remote_side=[id], back_populates="subcategories")
    subcategories = relationship("Category", back_populates="parent")
    products = relationship("Product", back_populates="category")
