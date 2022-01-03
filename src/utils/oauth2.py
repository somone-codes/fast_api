import datetime
from os import getenv

from jose import jwt

SECRET_KEY = getenv("TOKEN_SECRET_KEY")
ALGORITHM = getenv("TOKEN_ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(getenv("TOKEN_EXPIRE"))


def create_token(data: dict,
                 secret_key: str = SECRET_KEY,
                 algorithm: str = ALGORITHM,
                 expiry: int = ACCESS_TOKEN_EXPIRE_MINUTES) -> str:
    data_to_encode = data.copy()
    expiry = datetime.datetime.now() + datetime.timedelta(minutes=float(expiry))
    data_to_encode.update({"exp": expiry})

    return jwt.encode(data_to_encode, secret_key, algorithm)



