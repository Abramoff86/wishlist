from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, Float
from sqlalchemy.orm import relationship

from app.backend.db import Base


class Desire(Base):
    __tablename__ = 'disires'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    link = Column(String)
    price = Column(Integer)
    willing_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    is_active = Column(Boolean, default=True)
    reservation = Column(Boolean, default=False)

    user = relationship('User', back_populates='disires')