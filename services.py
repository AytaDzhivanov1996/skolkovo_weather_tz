import pandas as pd
import asyncio
import aiohttp
import aioconsole
import os

from sqlalchemy import select
from dotenv import load_dotenv

from database import async_session, WeatherData

env_path = '.env'
load_dotenv(dotenv_path=env_path, override=True)

async def fetch_weather_data(session):
    """Функция запроса данных по API"""
    url = f"http://api.weatherapi.com/v1/current.json?key={os.getenv('API_KEY')}&q=Инновационный центр Сколково&aqi=no&lang=ru"
    async with session.get(url) as response:
        data = await response.json()
        current_weather = data["current"]
        wind_speed = round(current_weather["wind_kph"] / 3.6, 1)
        atm_pressure = round(current_weather["pressure_mb"] * 0.750063755419211)
        return {
            "temperature": f"{current_weather['temp_c']}°C",
            "wind_speed": f"{wind_speed} м/с",
            "wind_direction": current_weather["wind_dir"],
            "atm_pressure": f"{atm_pressure} мм рт.ст.",
            "description": current_weather["condition"]["text"],
            "precipitation_amount": f"{current_weather['precip_mm']} мм"
        }

async def save_weather_data(data):
    """Сохранение данных в таблицу"""
    async with async_session() as session:
        async with session.begin():
            try:
                weather_data = WeatherData(
                    temperature=data["temperature"],
                    wind_speed=data["wind_speed"],
                    wind_direction=data["wind_direction"],
                    atm_pressure=data["atm_pressure"],
                    description=data["description"],
                    precipitation_amount=data["precipitation_amount"]
                )
                session.add(weather_data)
            except Exception as e:
                print(f"Ошибка при сохранении данных: {e}")

async def export_to_excel():
    """Экспорт в Excel"""
    async with async_session() as session:
        async with session.begin():
            try:
                results = await session.execute(
                    select(WeatherData).order_by(WeatherData.id.desc()).limit(10)
                )
                weather_data = results.scalars().all()
                if not weather_data:
                    print("Нет данных для экспорта")
                    return
                
                data = []
                for entry in weather_data:
                    data.append({
                        "Температура": entry.temperature,
                        "Скорость ветра": entry.wind_speed,
                        "Направление ветра": entry.wind_direction,
                        "Атмосферное давление": entry.atm_pressure,
                        "Краткое описание": entry.description,
                        "Кол-во осадков": entry.precipitation_amount
                    })
                
                df = pd.DataFrame(data)

                file_path = "weather_data.xlsx"
                df.to_excel(file_path, index=False)
                print(f"Данные о погоде экспортированы в файл {file_path}.")
            except Exception as e:
                print(f"Ошибка при экспорте данных: {e}")

async def weather_update():
    """Постонное обновление и добавление данных о погоде с 10-минутным интервалом"""
    async with aiohttp.ClientSession() as session:
        while True:
            weather_data = await fetch_weather_data(session)
            if weather_data and weather_data["temperature"] is not None:
                await save_weather_data(weather_data)
            else:
                print("Данные о погоде не получены или не полны.")
            await asyncio.sleep(5)

async def command_listener():
    """Хендлер для команд export и exit"""
    while True:
        command = await aioconsole.ainput("Введите команду (export для экспорта данных в Excel или exit для выхода из программы):\n")
        print(f"Вы ввели команду: {command}")
        if command.lower() == "export":
            await export_to_excel()
        elif command.lower() == "exit":
            print("Завершение программы...")
            break
