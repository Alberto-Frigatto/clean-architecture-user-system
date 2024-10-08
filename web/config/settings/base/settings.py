from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    api_title: str
    access_token_expire_minutes: int = 180
    jwt_algorithm: str = 'HS256'
    mongo_database: str
    mongo_uri: str
    secret_key: str
