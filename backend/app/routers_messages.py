from datetime import datetime, timezone
from pathlib import Path
from typing import List
from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from sqlalchemy.orm import Session

from .auth import get_current_user
from .database import get_db
from .models import Message, Attachment, User
from .schemas import MessageOut, MessageCreate, MessageUpdate, AttachmentOut
from .config import settings

router = APIRouter(prefix="/messages", tags=["messages"])

UPLOAD_DIR = Path(settings.UPLOAD_DIR)
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

@router.post("/", response_model=MessageOut)
def send_message(
    recipient_id: int = Form(...),
    content: str | None = Form(None),
    files: List[UploadFile] | None = File(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # Prevent completely empty messages (no text and no attachments)
    if (content is None or str(content).strip() == "") and (not files or len(files) == 0):
        raise HTTPException(status_code=400, detail="Message must have text or attachments")
    if current_user.id == recipient_id:
        raise HTTPException(status_code=400, detail="Cannot send message to yourself")
    recipient = db.query(User).filter(User.id == recipient_id).first()
    if not recipient:
        raise HTTPException(status_code=404, detail="Recipient not found")
    msg = Message(sender_id=current_user.id, recipient_id=recipient_id, content=content)
    db.add(msg)
    db.commit()
    db.refresh(msg)

    saved_attachments: list[Attachment] = []
    if files:
        for f in files:
            safe_name = f"{msg.id}_{int(datetime.now(timezone.utc).timestamp())}_{f.filename}"
            dest = UPLOAD_DIR / safe_name
            with dest.open("wb") as out:
                out.write(f.file.read())
            att = Attachment(message_id=msg.id, file_path=str(dest), file_name=f.filename)
            db.add(att)
            saved_attachments.append(att)
        db.commit()

    db.refresh(msg)
    return serialize_message(msg)

@router.get("/thread/{other_user_id}", response_model=list[MessageOut])
def get_thread(other_user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
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

@router.patch("/{message_id}", response_model=MessageOut)
def update_message(message_id: int, patch: MessageUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    msg = db.query(Message).filter(Message.id == message_id).first()
    if not msg or msg.sender_id != current_user.id:
        raise HTTPException(status_code=404, detail="Message not found")
    if patch.content is not None:
        msg.content = patch.content
    msg.updated_at = datetime.now(timezone.utc)
    if patch.deleted is True:
        msg.deleted = True
    db.commit()
    db.refresh(msg)
    return serialize_message(msg)

@router.delete("/{message_id}", status_code=204)
def delete_message(message_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    msg = db.query(Message).filter(Message.id == message_id).first()
    if not msg or msg.sender_id != current_user.id:
        raise HTTPException(status_code=404, detail="Message not found")
    # Hard delete: remove attachment files and delete the message row
    atts = db.query(Attachment).filter(Attachment.message_id == msg.id).all()
    for a in atts:
        try:
            Path(a.file_path).unlink(missing_ok=True)
        except Exception:
            pass
    db.delete(msg)
    db.commit()


def serialize_message(m: Message) -> MessageOut:
    base_url = "/uploads"  # served by backend static mount
    return MessageOut(
        id=m.id,
        sender_id=m.sender_id,
        recipient_id=m.recipient_id,
        content=m.content,
        created_at=m.created_at,
        updated_at=m.updated_at,
        deleted=m.deleted,
        attachments=[
            AttachmentOut(
                id=a.id,
                file_name=a.file_name,
                file_url=f"{base_url}/{Path(a.file_path).name}",
                uploaded_at=a.uploaded_at,
            )
            for a in getattr(m, "attachments", [])
        ],
    )
