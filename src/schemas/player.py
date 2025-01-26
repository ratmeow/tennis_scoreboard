from pydantic import BaseModel, ConfigDict, Field


class Player(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)

