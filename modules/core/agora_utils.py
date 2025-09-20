import os
import time
from agora_token_builder import RtcTokenBuilder

APP_ID = os.getenv("AGORA_APP_ID")
APP_CERTIFICATE = os.getenv("AGORA_APP_CERTIFICATE")

def generate_agora_token(channel_name: str, uid: int):
    expiration_time_in_seconds = 3600  # 1 hour
    current_timestamp = int(time.time())
    privilege_expired_ts = current_timestamp + expiration_time_in_seconds

    token = RtcTokenBuilder.buildTokenWithUid(
        APP_ID, APP_CERTIFICATE, channel_name, uid,
        1, privilege_expired_ts
    )
    return token
