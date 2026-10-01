from datetime import datetime, timedelta, timezone
import config
import jwt

def create_access_token(data: dict):
    payload = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(
        minutes = config.ACCESS_TOKEN_EXPIRE_MINUTES
    )

    payload["exp"] = expire

    return jwt.encode(
        payload,
        config.JWT_SECRET,
        algorithm = config.JWT_ALGORITHM
    )
