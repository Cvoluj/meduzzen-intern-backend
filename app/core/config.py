from pydantic_settings import BaseSettings, SettingsConfigDict


class ServerSettings(BaseSettings):
    HOST: str
    PORT: int
    RELOAD: bool
    LOG_LEVEL: str
    
    model_config = SettingsConfigDict(env_file='.env')


if __name__ == '__main__': # code snippet 
    server_setting = ServerSettings()
    print(server_setting.HOST)
    print(server_setting.PORT)
    print(server_setting.RELOAD)
    print(server_setting.LOG_LEVEL)