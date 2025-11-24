from sqlalchemy.orm import  mapped_column
from configurations.db_config import Base
from sqlalchemy import Integer, String


class User(Base):
    __tablename__ = "users"
    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String(100))
    email = mapped_column(String(200))
    
    
