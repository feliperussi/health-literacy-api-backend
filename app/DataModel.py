from pydantic import BaseModel


class DataModel(BaseModel):
    text: str

class DataModel_2(BaseModel):
    text: str
    feature: str
