import os

from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy import Column, Integer, String
from dotenv import load_dotenv

env_path = '.env'
load_dotenv(dotenv_path=env_path, override=True)

#Подключение к БД
Base = declarative_base()
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_async_engine(DATABASE_URL)
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

class WeatherData(Base):
    """Модель данных о погоде"""
    __tablename__ = "weather_data"

    id = Column(Integer, primary_key=True, autoincrement=True)
    temperature = Column(String(10))
    wind_speed = Column(String(10))
    wind_direction = Column(String(10))
    atm_pressure = Column(String(20))
    description = Column(String(64))
    precipitation_amount = Column(String(10))