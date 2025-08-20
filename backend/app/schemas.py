from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, EmailStr, ConfigDict

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    user_id: int

class UserBase(BaseModel):
    email: EmailStr
    username: str

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class UserOut(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)

class AttachmentOut(BaseModel):
    id: int
    file_name: str
    file_url: str
    uploaded_at: datetime
    model_config = ConfigDict(from_attributes=True)

class MessageBase(BaseModel):
    content: Optional[str] = None

class MessageCreate(MessageBase):
    recipient_id: int

class MessageUpdate(BaseModel):
    content: Optional[str] = None
    deleted: Optional[bool] = None

class MessageOut(MessageBase):
    id: int
    sender_id: int
    recipient_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    deleted: bool
    attachments: List[AttachmentOut] = []
    model_config = ConfigDict(from_attributes=True)
