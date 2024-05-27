import sys
import os
import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, URLInputFile

from game import Game

if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


class Form(StatesGroup):
    settings = State()


games = {}
settings = {}
logging.basicConfig(level=logging.INFO, stream=sys.stdout)
dp = Dispatcher()
bot = Bot(token=os.environ.get('BOT_TOKEN'))


@dp.message(Command("start"))
async def handler(message: Message):
    await message.answer(f'Привет, {message.from_user.full_name}!')


@dp.message(Command("newgame"))
async def handler(message: Message):
    games[message.from_user.id] = Game(settings=settings.get(message.from_user.id, None))

    try:
        answer = await games[message.from_user.id].start()

        try:
            image = URLInputFile(answer['image'])
            await message.answer_photo(image, caption=answer['text'])

        except Exception as e:
            print(e)
            await message.answer(answer['text'])

    except Exception as e:
        await message.answer(f'Ошибка: {e}')


@dp.message(Command("settings"))
async def handler(message: Message, state: FSMContext):
    await message.answer('Героем какой истории вы бы хотели стать?')
    await state.set_state(Form.settings)


@dp.message(Form.settings)
async def handler(message: Message, state: FSMContext):
    settings[message.from_user.id] = message.text
    await state.clear()
    await message.answer('История настроена!')


@dp.message()
async def handler(message: Message):
    if games.get(message.from_user.id, None) is None:
        await message.answer("Начните игру")

    else:
        try:
            answer = await games[message.from_user.id].move(message.text)
            try:
                if answer['code'] == '1':
                    image = URLInputFile(answer['image'])
                    await message.answer_photo(image, caption=answer['text'])

                elif answer['code'] == '2':
                    image = URLInputFile(answer['image'])
                    await message.answer_photo(image, caption=answer['text'])
                    del games[message.from_user.id]

                else:
                    await message.answer(answer['text'])

            except Exception:
                await message.answer(answer['text'])

        except Exception as e:
            await message.answer(f'Ошибка: {e}')


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
