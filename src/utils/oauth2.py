import datetime
from os import getenv
from typing import List, Optional, Any

from jose import jwt

SECRET_KEY = getenv("TOKEN_SECRET_KEY")
ALGORITHM = getenv("TOKEN_ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(getenv("TOKEN_EXPIRE"))


def create_token(data: dict,
                 secret_key: str = SECRET_KEY,
                 algorithm: str = ALGORITHM,
                 expiry: int = ACCESS_TOKEN_EXPIRE_MINUTES) -> str:
    data_to_encode = data.copy()
    expiry = datetime.datetime.utcnow() + datetime.timedelta(minutes=float(expiry))
    data_to_encode.update({"exp": expiry})

    return jwt.encode(data_to_encode, secret_key, algorithm)


def validate_token(token,
                   payload_key: List[str],
                   schema: Optional[Any],
                   secret_key: str = SECRET_KEY,
                   algorithm: str = ALGORITHM,
                   invalid_creds_error: Exception = jwt.JWTError("Invalid API Token.")):
    try:
        payload = jwt.decode(token, secret_key, [algorithm])
        _validate_payload(payload, payload_key)
        if schema:
            return schema(**payload)
        return payload
    except jwt.JWTError:
        raise invalid_creds_error


def _validate_payload(payload: dict, keys: List[str]):
    for key in keys:
        if not payload.get(key):
            return False
    else:
        return True
