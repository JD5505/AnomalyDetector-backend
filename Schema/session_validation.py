from pydantic import BaseModel, EmailStr, Field
from datetime import datetime

class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
    role: str

class VerifyOTPRequest(BaseModel):
    email: EmailStr
    otp: str = Field(min_length=6, max_length=6, pattern=r"^\d{6}$")

class VerifyLogin(BaseModel):
    email: EmailStr
    password: str

class LocationRequest(BaseModel):
    latitude: float
    longitude: float
    timestamp: datetime

class EnterNewPassword(BaseModel):
    email: EmailStr
    password : str