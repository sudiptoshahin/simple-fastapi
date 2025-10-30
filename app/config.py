from pydantic_settings import BaseSettings

# In production we have to set these variables 
# to the system variables

class Settings(BaseSettings):
    database_hostname: str
    database_port: str
    database_password: str
    database_name: str
    database_username: str
    secret_key: str
    algorithm: str
    access_token_expire_minuites: int

    class Config:
        env_file = ".env"


settings = Settings()