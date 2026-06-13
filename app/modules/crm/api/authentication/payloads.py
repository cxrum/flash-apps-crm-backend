from pydantic import BaseModel, Field


class UserRegistrationSchemaPayload(BaseModel):
    login: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=8)
    full_name: str = Field(min_length=2, max_length=100)
    timezone: str 