import sys

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.utils import executor

from uploader import upload_video, register

from config import token
bot = Bot(token=token)
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

if __name__ == '__main__':
    if len(sys.argv) > 1:
        if sys.argv[1] == 'auth':
            register()
        else:
            sys.exit()
    else:

        executor.start_polling(dp, skip_updates=True, on_startup=register)