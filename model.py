from db import Base
from sqlalchemy import Column, Integer, String

class Book(Base):
    __tablename__ = "book"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), index=True)
    author = Column(String(255), index=True)
    description = Column(String(1000))