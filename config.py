from pydantic import EmailStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Awesome API"
    admin_email: EmailStr
    items_per_user: int = 50


class DotenvSettings(BaseSettings):
    app_name: str = "Awesome API"
    admin_email: EmailStr
    items_per_user: int = 50

    model_config = SettingsConfigDict(env_file=".env")
