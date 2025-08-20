from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from typing import List, Dict
from jose import jwt, JWTError
from .config import settings

router = APIRouter(prefix="/demo", tags=["demo"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

# Mock DB
messages_db: List[Dict[str, str]] = [
    {"id": "1", "text": "Hello!", "user_id": "1"},
    {"id": "2", "text": "How are you?", "user_id": "2"},
    {"id": "3", "text": "This will be deleted", "user_id": "1"},
]

class Message(BaseModel):
    id: str
    text: str
    user_id: str

def decode_jwt_user_id(token: str) -> str | None:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        sub = payload.get("sub")
        return str(sub) if sub is not None else None
    except JWTError:
        return None

async def get_current_user(token: str = Depends(oauth2_scheme)):
    user_id = decode_jwt_user_id(token)
    if not user_id:
        # fallback: token itself as identifier
        user_id = token
    return user_id

@router.get("/messages", response_model=List[Message])
async def get_messages(current_user: str = Depends(get_current_user)):
    return [Message(**m) for m in messages_db]

@router.delete("/messages/{message_id}")
async def delete_message(message_id: str, current_user: str = Depends(get_current_user)):
    global messages_db
    for msg in messages_db:
        if msg["id"] == message_id:
            if msg["user_id"] != current_user:
                raise HTTPException(status_code=403, detail="Not allowed to delete this message")
            messages_db = [m for m in messages_db if m["id"] != message_id]
            return {"detail": "Message deleted"}
    raise HTTPException(status_code=404, detail="Message not found")
