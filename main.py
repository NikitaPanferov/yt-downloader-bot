import os
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.utils import executor

from uploader import upload_video

import dotenv

dotenv.load_dotenv()

bot = Bot(token=os.getenv('BOT_TOKEN'))
dp = Dispatcher(bot, storage=MemoryStorage())

class States(StatesGroup):
    start = State()
    waiting = State()

@dp.message_handler(commands=['download'])
async def download(message: types.Message):
    await States.start.set()
    await message.answer('Пришлите URL видео')


@dp.message_handler(state=States.start)
async def waiting(message: types.Message, state: FSMContext):
    await state.finish()
    mes = await message.answer('Ожидайте')
    video_id = await upload_video(message.text, mes)
    await message.answer_video(video_id)


@dp.message_handler(commands=['help', 'start'])
async def help(message: types.Message):
    await message.answer('Используй комманду /download')


# @dp.message_handler(commands=['vid'])
# async def vid(message: types.Message):
#     await message.answer(message.text.split(' ')[1].strip())
#     await message.answer_video(message.text.split(' ')[1].strip())


executor.start_polling(dp, skip_updates=True)