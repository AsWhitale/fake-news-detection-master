from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    SQLALCHEMY_DATABASE_URL: str = "mysql+pymysql://root:123@localhost:3306/fake_news_detection"
    MODEL_PATH: str = "./models/trained_model.pkl"

    class Config:
        env_file = ".env"


settings = Settings()
