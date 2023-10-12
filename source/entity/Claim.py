from pydantic import BaseModel


class Claim(BaseModel):
    idx: int
    text: str
