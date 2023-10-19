from pydantic_settings import BaseSettings, SettingsConfigDict


class ServerSettings(BaseSettings):
    PORT: int
    DB_HOST: str
    DB_PORT: int
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    REDIS_HOST: str

    @property
    def DB_URL(self):
        return f'postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@postgres:{self.DB_PORT}/{self.POSTGRES_DB}'        

    model_config = SettingsConfigDict(env_file='.env')


server_setting = ServerSettings()