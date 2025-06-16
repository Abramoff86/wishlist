from pydantic import BaseModel

class CreateDesire(BaseModel):
    name: str
    link: str
    price: int


class CreateUser(BaseModel):
    first_name: str
    last_name: str
    username: str
    email: str
    password: str

