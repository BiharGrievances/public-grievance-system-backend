from pydantic import BaseModel, EmailStr, constr

class UserBase(BaseModel):
    name: constr(min_length=1)
    email: EmailStr
