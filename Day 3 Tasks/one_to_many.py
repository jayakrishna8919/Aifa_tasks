#one to many
from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    posts = relationship("Post", back_populates="user")

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    content = Column(String(500))

    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="posts")
