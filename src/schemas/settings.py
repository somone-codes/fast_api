from pydantic import BaseSettings


class Settings(BaseSettings):
    SQLALCHEMY_DATABASE_URL: str
    TOKEN_SECRET_KEY: str
    TOKEN_EXPIRE: int
    TOKEN_ALGORITHM: str
    TOKEN_URL: str
    ALEMBIC_SQLALCHEMY_DATABASE_URL: str

    class Config:
        env_file = ".env"


settings = Settings()
