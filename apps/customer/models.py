from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from db.session import Base


class Customer(Base):
    __tablename__ = "customers"

    id: int = Column(Integer, primary_key=True)
    name: str = Column(String(255))
    phone: str = Column(String(255))
    store_id: int = Column(ForeignKey('stores.id'), nullable=False)

    order = relationship('Order', back_populates='customer')
    store = relationship('Store', back_populates='customer')
    visit = relationship('Visit', back_populates='customer')

    def __str__(self):
        return f'{self.name}'
