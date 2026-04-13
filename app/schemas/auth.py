from pydantic import BaseModel, EmailStr, Field


class RegisterRequest(BaseModel):
    email: EmailStr = Field(..., example="student_ivanov@email.com")
    password: str = Field(..., min_length=8, example="strongpassword")


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"