from datetime import datetime, timezone
from pathlib import Path
import shutil
import re
import aiofiles
from typing import List, Union
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

def sanitize_filename(filename: str) -> str:
    """
    Sanitizes a filename by removing or replacing characters that are not
    suitable for file systems.
    """
    # Replace spaces with underscores
    filename = filename.replace(" ", "_")
    # Remove any characters that are not alphanumeric, underscore, dot, or hyphen
    # This is a basic sanitization, more complex logic might be needed for
    # production systems (e.g., handling path traversal, etc.)
    return re.sub(r'(?u)[^-\w.]', '', filename)

@router.post("/", response_model=MessageOut)
async def send_message(
    recipient_id: int | None = Form(None),
    receiver_id: int | None = Form(None),
    content: str | None = Form(None),
    files: Union[List[UploadFile], UploadFile, None] = File(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # Accept both recipient_id and receiver_id for compatibility
    if recipient_id is None and receiver_id is None:
        raise HTTPException(status_code=422, detail="recipient_id or receiver_id is required")
    final_recipient_id = recipient_id if recipient_id is not None else receiver_id
    
    # Normalize files to always be a list
    if files is not None:
        if not isinstance(files, list):
            files = [files]
    
    # Prevent completely empty messages (no text and no attachments)
    if (content is None or str(content).strip() == "") and (not files or len(files) == 0):
        raise HTTPException(status_code=400, detail="Message must have text or attachments")
    if current_user.id == final_recipient_id:
        raise HTTPException(status_code=400, detail="Cannot send message to yourself")
    recipient = db.query(User).filter(User.id == final_recipient_id).first()
    if not recipient:
        raise HTTPException(status_code=404, detail="Recipient not found")
    msg = Message(sender_id=current_user.id, recipient_id=final_recipient_id, content=content)
    db.add(msg)
    db.commit()
    db.refresh(msg)

    if files:
        # Ensure the main upload directory exists
        UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
        for f in files:
            # Skip empty file form fields
            if not f.filename:
                continue
            try:
                # Sanitize filename to prevent security issues
                original_name = f.filename
                sanitized = sanitize_filename(original_name)
                
                # Handle cases where sanitization results in an empty string
                if not sanitized:
                    sanitized = "unnamed_file"

                # Create a unique filename to avoid overwrites
                safe_name = f"{msg.id}_{int(datetime.now(timezone.utc).timestamp())}_{sanitized}"
                dest = UPLOAD_DIR / safe_name
                
                # Save the file asynchronously
                contents = await f.read()
                if contents:  # Proceed only if file is not empty
                    async with aiofiles.open(dest, "wb") as out_file:
                        await out_file.write(contents)
                    
                    # Create and add attachment record to the session
                    att = Attachment(message_id=msg.id, file_path=str(dest), file_name=original_name)
                    db.add(att)
                
            except Exception as e:
                # Provide a more informative error message
                raise HTTPException(status_code=500, detail=f"Could not save file: {f.filename}. Error: {str(e)}")
        
        # Commit all new attachments at once
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
    msg = db.query(Message).filter(Message.id == message_id, Message.sender_id == current_user.id).first()

    if msg and not msg.deleted:
        # Soft delete the message
        msg.deleted = True
        msg.updated_at = datetime.now(timezone.utc)
        db.commit()

    # If the message doesn't exist, isn't owned, or is already deleted,
    # we do nothing and return 204. This makes the action idempotent
    # and prevents errors on the frontend, ensuring the message stays hidden.


def serialize_message(m: Message) -> MessageOut:
    base_url = "/uploads"  # served by backend static mount
    files_simple = [f"{base_url}/{Path(a.file_path).name}" for a in getattr(m, "attachments", [])]
    return MessageOut(
        id=m.id,
        sender_id=m.sender_id,
        recipient_id=m.recipient_id,
        receiver_id=m.recipient_id,
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
        files=files_simple or None,
    )
