from pydantic import BaseModel


class ShowCustomer(BaseModel):
    id: int
    name: str
    phone: str

    class Config:
        orm_mode = True
