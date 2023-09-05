from datetime import datetime

from sqlalchemy import TIMESTAMP, Integer
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.sql.schema import Column, ForeignKey

from apps.order.models import Order
from db.session import Base


class Visit(Base):
    __tablename__: str = "visits"

    id: int = Column(Integer, primary_key=True)
    creation_time: datetime = Column(
        TIMESTAMP(timezone=True), default=datetime.now()
    )
    executor_id: int = Column(ForeignKey('workers.id'), nullable=False)
    order_id: int = Column(ForeignKey('orders.id'))
    order: Mapped[Order] = relationship('Order', uselist=False,
                                        backref="visit")
    author_id: int = Column(ForeignKey('customers.id'), nullable=False)
    store_id: int = Column(ForeignKey('stores.id'), nullable=False)

    customer = relationship('Customer', back_populates='visit')
    worker = relationship('Worker', back_populates='visit')
    store = relationship('Store', back_populates='visit')

    def __str__(self):
        return f'Посещение #{self.id}'
