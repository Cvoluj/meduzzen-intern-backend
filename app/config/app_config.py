from pydantic_settings import BaseSettings, SettingsConfigDict


class ServerSettings(BaseSettings):
    JWT_SECRET_KEY: str
    JWT_REFRESH_SECRET_KEY: str
    PORT: int
    DB_HOST: str
    DB_PORT: int
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    REDIS_HOST: str
    DOMAIN: str
    API_AUDIENCE: str
    ISSUER: str
    AUTH0_ALGORITHM: str


    @property
    def DB_URL(self):
        return f'postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@localhost:{self.DB_PORT}/{self.POSTGRES_DB}'        

    model_config = SettingsConfigDict(env_file='.env')


server_setting = ServerSettings()