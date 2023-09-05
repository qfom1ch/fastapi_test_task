from sqlalchemy import Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import Column, ForeignKey, Table

from db.session import Base

stores_mtm_workers_table = Table(
    'stores_mtm_workers',
    Base.metadata,
    Column('id', Integer, primary_key=True),
    Column('stores_id', Integer, ForeignKey('stores.id'), nullable=False),
    Column('workers_id', Integer, ForeignKey('workers.id'), nullable=False),
)


class Store(Base):
    __tablename__: str = "stores"

    id: int = Column(Integer, primary_key=True)
    name: str = Column(String(255))

    workers = relationship('Worker',
                           secondary=stores_mtm_workers_table,
                           back_populates='stores')
    order = relationship('Order', back_populates='store')
    customer = relationship('Customer', back_populates='store')
    visit = relationship('Visit', back_populates='store')

    def __str__(self):
        return f'{self.name}'
