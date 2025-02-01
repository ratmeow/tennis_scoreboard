from pydantic import BaseModel, ConfigDict


class Player(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)
