from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_USER_NAME : str
    DATABASE_PASSWORD : str 
    DATABASE_HOST : str
    DATABASE_NAME : str

    class Config:
        env_file = ".env"

settings = Settings()