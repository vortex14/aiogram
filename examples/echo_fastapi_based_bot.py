from aiogram import Bot, Dispatcher, types
from fastapi import FastAPI
import logging
import asyncio

API_TOKEN = "<TOKEN>"

logging.basicConfig(level=logging.DEBUG)

class AsyncioBot:

    # Initialize bot and dispatcher
    def __init__(self) -> None:
        self.bot = Bot(token=API_TOKEN)
        self.dp = Dispatcher(self.bot)

        self.dp.register_message_handler(self.on_message)

    async def on_message(self, message: types.Message):
        print(message.get_command())
        await message.answer(f"Asnwer: {message.text}")

    async def run(self):
        # await self.dp.start_polling() # will be blocking main :on_start: FastAPI event
        asyncio.create_task(self.dp.start_polling())

    async def close(self):
        bot = self.bot.get_session()
        bot.close()


app = FastAPI()
bot = AsyncioBot()

@app.on_event("startup")
async def on_startup():
    await bot.run()

@app.get("/")
async def root():
    return {"data": "Hello World"}

@app.on_event("shutdown")
async def on_shutdown():
    await bot.close() # closing bot without error
