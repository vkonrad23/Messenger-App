from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .auth import get_current_user
from .database import get_db
from .models import Message, User
from .schemas import MessageOut
from .routers_messages import serialize_message


router = APIRouter(tags=["threads"])


@router.get("/threads/{other_user_id}/messages", response_model=List[MessageOut])
def list_messages(other_user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    messages = (
        db.query(Message)
        .filter(
            ((Message.sender_id == current_user.id) & (Message.recipient_id == other_user_id))
            | ((Message.sender_id == other_user_id) & (Message.recipient_id == current_user.id))
        )
        .filter(Message.deleted == False)
        .order_by(Message.created_at.asc())
        .all()
    )
    return [serialize_message(m) for m in messages]


    
