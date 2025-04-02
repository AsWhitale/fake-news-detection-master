from pydantic import BaseModel, EmailStr, ConfigDict


class HistoryQuery(BaseModel):
    page: int
    page_size: int

class UserLogin(BaseModel):
    username: str
    password: str

    model_config = ConfigDict(from_attributes=True)