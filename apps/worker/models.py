from sqlalchemy import Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import Column

from apps.store.models import stores_mtm_workers_table
from db.session import Base


class Worker(Base):
    __tablename__: str = "workers"

    id: int = Column(Integer, primary_key=True)
    name: str = Column(String(255))
    phone: str = Column(String(255))

    stores = relationship('Store',
                          secondary=stores_mtm_workers_table,
                          back_populates='workers')

    order = relationship('Order', back_populates='worker')
    visit = relationship('Visit', back_populates='worker')

    def __str__(self):
        return f'{self.name}'
