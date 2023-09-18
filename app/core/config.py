from pydantic_settings import BaseSettings, SettingsConfigDict


class ServerSettings(BaseSettings):
    HOST: str
    PORT: int
    RELOAD: bool
    
    model_config = SettingsConfigDict(env_file='.env')


if __name__ == '__main__': # code snippet 
    server_setting = ServerSettings().model_dump()
    print(server_setting)