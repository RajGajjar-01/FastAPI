from pydantic import BaseModel, EmailStr

class UserInCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: str

class UserOutput(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: EmailStr

class UserInUpdate(BaseModel):
    id: int
    first_name: str | None = None
    last_name: str | None = None
    email: EmailStr | None = None
    password: str | None = None

class UserInLogin(BaseModel):
    email: EmailStr
    password: str

class UserWithToken(BaseModel):
    token: str