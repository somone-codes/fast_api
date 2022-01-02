from passlib.context import CryptContext

context = CryptContext(schemes='bcrypt', deprecated="auto")


def encrypt(password: str) -> str:
    return context.hash(password)
