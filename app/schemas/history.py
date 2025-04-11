from pydantic import BaseModel, ConfigDict


class HistoryQuery(BaseModel):
    page: int
    page_size: int


class HistoryQueryFilter(BaseModel):
    page: int
    page_size: int
    filter: str

    model_config = ConfigDict(from_attributes=True)
