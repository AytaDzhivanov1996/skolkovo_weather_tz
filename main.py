import asyncio

from services import weather_update, command_listener

async def main():
    task = asyncio.create_task(weather_update())

    await command_listener()
    task.cancel()

if __name__ == "__main__":
    asyncio.run(main())
