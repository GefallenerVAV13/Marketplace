from sqlalchemy import String, Numeric, ForeignKey, Text, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

class Product(Base):
    __tablename__ = "products"

    id:Mapped[int] = mapped_column(primary_key=True, index=True)
    title:Mapped[str] = mapped_column(String(255), index=True, nullable=False)
    description:Mapped[str | None] = mapped_column(Text, nullable=True)
    price:Mapped[int] = mapped_column(Numeric(10, 2), nullable=False)
    stock:Mapped[int] = mapped_column(Integer, default=0, nullable=False)
