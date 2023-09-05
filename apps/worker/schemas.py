from pydantic import BaseModel


class ShowStore(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class ShowWorker(BaseModel):
    id: int
    name: str
    phone: str

    class Config:
        orm_mode = True
