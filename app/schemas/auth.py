from pydantic import BaseModel, Field

class UserRegister(BaseModel):

    username: str = Field(min_length=3, max_length=15)
    email: str
    password: str = Field(min_length=6)


class UserLogin(BaseModel):

    username: str
    password: str