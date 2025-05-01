from dotenv import find_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=find_dotenv(),
    )

    FSTR_DB_HOST: str
    FSTR_DB_PORT: str
    FSTR_DB_LOGIN: str
    FSTR_DB_PASS: str
    FSTR_DB_NAME: str

    @property
    def async_database_url(self):
        return (f"postgresql+asyncpg://{self.FSTR_DB_LOGIN}:{self.FSTR_DB_PASS}"
                f"@{self.FSTR_DB_HOST}:{self.FSTR_DB_PORT}/{self.FSTR_DB_NAME}")


settings = Settings()
