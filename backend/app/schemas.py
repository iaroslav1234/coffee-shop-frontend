from pydantic import BaseModel, EmailStr
from typing import Optional, List, Dict
from datetime import datetime

class Token(BaseModel):
    access_token: str
    token_type: str
    user: Dict

class GoogleToken(BaseModel):
    token: str
    email: str
    name: Optional[str] = None
    picture: Optional[str] = None

class TokenData(BaseModel):
    email: Optional[str] = None

class EmailSchema(BaseModel):
    email: EmailStr

class PasswordReset(BaseModel):
    token: str
    new_password: str

class UserBase(BaseModel):
    email: str
    name: Optional[str] = None
    picture: Optional[str] = None

class UserCreate(UserBase):
    password: Optional[str] = None

class User(UserBase):
    id: int
    is_active: bool

    class Config:
        orm_mode = True

class InventoryBase(BaseModel):
    name: str
    current_stock: float
    unit: str
    min_threshold: float
    threshold_unit: str

class InventoryCreate(InventoryBase):
    pass

class Inventory(InventoryBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class SaleBase(BaseModel):
    amount: float
    items: List[dict]
    payment_method: str

class SaleCreate(SaleBase):
    pass

class Sale(SaleBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
