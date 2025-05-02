from dotenv import find_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict


# Создать класс с настройками всего приложения.
class Settings(BaseSettings):
    # Загрузить переменные из окружения.
    model_config = SettingsConfigDict(
        env_file=find_dotenv(),
    )

    # Провалидировать данные для подключения к базе данных.
    FSTR_DB_PORT: str
    FSTR_DB_LOGIN: str
    FSTR_DB_PASS: str
    FSTR_DB_NAME: str

    # Создать свойство, генерирующее ссылку для подключения к базе данных.
    @property
    def async_database_url(self):
        return (f"postgresql+asyncpg://{self.FSTR_DB_LOGIN}:{self.FSTR_DB_PASS}"
                f"@{self.FSTR_DB_HOST}:{self.FSTR_DB_PORT}/{self.FSTR_DB_NAME}")


# Сохранить настройки проекта в переменную.
settings = Settings()
