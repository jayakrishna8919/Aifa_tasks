from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Date, Float, Enum as SAEnum
from database.config import Base
from datetime import datetime
import enum
from sqlalchemy.orm import relationship
class RoleEnum(str, enum.Enum):
    user = "user"
    librarian = "librarian"
    admin = "admin"

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(120), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role = Column(SAEnum(RoleEnum), default=RoleEnum.user, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)

    borrows = relationship("Borrow", back_populates="user", cascade="all, delete-orphan")

class Book(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    author = Column(String(255), nullable=True)
    isbn = Column(String(50), unique=True, nullable=True)
    total_copies = Column(Integer, default=1)
    available_copies = Column(Integer, default=1)
    created_at = Column(DateTime, default=datetime.utcnow)

    borrows = relationship("Borrow", back_populates="book", cascade="all, delete-orphan")

class Borrow(Base):
    __tablename__ = "borrows"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    book_id = Column(Integer, ForeignKey("books.id", ondelete="CASCADE"))
    borrowed_at = Column(DateTime, default=datetime.utcnow)
    due_date = Column(Date, nullable=False)
    returned_at = Column(DateTime, nullable=True)
    fine_amount = Column(Float, default=0.0)

    user = relationship("User", back_populates="borrows")
    book = relationship("Book", back_populates="borrows")

