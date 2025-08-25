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
    # Support both recipient_id and receiver_id for compatibility
    recipient_id: int
    # Optional alias field for clients using 'receiver_id'
    # Not used by validators here; router reads Form('recipient_id')

class MessageUpdate(BaseModel):
    content: Optional[str] = None
    deleted: Optional[bool] = None

class MessageOut(MessageBase):
    id: int
    sender_id: int
    recipient_id: int
    # Also expose receiver_id for compatibility with alternate clients
    receiver_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    deleted: bool
    # Existing rich attachment objects
    attachments: List[AttachmentOut] = []
    # Simple list of file URLs for lightweight clients
    files: Optional[List[str]] = None
    model_config = ConfigDict(from_attributes=True)
