# modules/video/routes.py
from fastapi import APIRouter, Depends, HTTPException
from modules.core.agora_utils import generate_agora_token
from modules.auth.security import get_current_user
from modules.users.models import User

router = APIRouter(prefix="/video", tags=["video"])

@router.get("/token")
def get_video_token(channel: str, current_user: User = Depends(get_current_user)):
    if not channel:
        raise HTTPException(status_code=400, detail="Channel name required")
    token = generate_agora_token(channel, current_user.id)
    return {
        "app_id": os.getenv("AGORA_APP_ID"),
        "channel": channel,
        "uid": current_user.id,
        "token": token
    }
