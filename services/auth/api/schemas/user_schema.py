import uuid

from pydantic import BaseModel, EmailStr


class UserSchema(BaseModel):
    email: EmailStr

class UserOutputSchema(UserSchema):
    id: uuid.UUID

class UserCreateSchema(UserSchema):
    password: str

    class Config:
        from_attributes = True
