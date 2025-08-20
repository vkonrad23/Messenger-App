from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from .config import settings
from .database import engine
from . import models
from .routers_auth import router as auth_router
from .routers_messages import router as messages_router
from .routers_demo import router as demo_router
from .routers_threads import router as threads_router
from .middleware import AuthMiddleware
from fastapi import Depends
from sqlalchemy.orm import Session
from .database import get_db
from .auth import get_current_user
from .models import User

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Messenger API")
app.add_middleware(AuthMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.BACKEND_CORS_ORIGINS],
    allow_credentials=True,
    allow_methods=["*"]
    ,allow_headers=["*"]
)

app.mount("/uploads", StaticFiles(directory=settings.UPLOAD_DIR), name="uploads")

app.include_router(auth_router)
app.include_router(messages_router)
app.include_router(demo_router)
app.include_router(threads_router)

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.get("/me")
def me(current_user: User = Depends(get_current_user)):
    return {"id": current_user.id, "username": current_user.username, "email": current_user.email}
