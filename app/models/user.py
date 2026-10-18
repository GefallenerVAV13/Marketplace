import enum

from sqlalchemy import String, Enum as SQLEnum, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base

class UserRole(str, enum.Enum):
     CUSTOMER = "customer"
     SELLER = "seller"
     ADMIN = "admin"

class User(Base):
    __tablename__ = "users"

    id:Mapped[int] = mapped_column(primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[UserRole] = mapped_column(SQLEnum(UserRole), default=UserRole.CUSTOMER, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    category_id:Mapped[int] = mapped_column(ForeignKey("categories.id"), nullable=False)
    seller_id:Mapped[int] = mapped_column("users.id", nullable=False)

    category = relationship("Category", back_populates="products")
    seller = relationship("User")