from passlib.context import CryptContext

context = CryptContext(schemes='bcrypt', deprecated="auto")


def encrypt(password: str) -> str:
    return context.hash(password)


def validate(encrypted_password, plain_password) -> bool:
    return context.verify(plain_password, encrypted_password)
