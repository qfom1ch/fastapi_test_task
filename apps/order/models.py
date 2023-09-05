import enum
from datetime import datetime

from sqlalchemy import TIMESTAMP, Enum, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import Column, ForeignKey

from db.session import Base


class Status(enum.Enum):
    started = 'started'
    ended = 'ended'
    in_process = 'in process'
    awaiting = 'awaiting'
    canceled = 'canceled'


class Order(Base):
    __tablename__: str = "orders"

    id: int = Column(Integer, primary_key=True)
    creation_time: datetime = Column(
        TIMESTAMP(timezone=True), default=datetime.now()
    )
    end_time: datetime = Column(TIMESTAMP(timezone=True))
    store_id: int = Column(ForeignKey('stores.id'), nullable=False)
    author_id: int = Column(ForeignKey('customers.id'), nullable=False)
    status: str = Column(Enum(Status))
    executor_id: int = Column(ForeignKey('workers.id'), nullable=False)

    worker = relationship('Worker', back_populates='order')
    store = relationship('Store', back_populates='order')
    customer = relationship('Customer', back_populates='order')

    def __str__(self):
        return f'Заказ #{self.id}'
