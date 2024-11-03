from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from keyboards import keyboard
from texts import hello_text
from db import db
router = Router()
kb = keyboard.Keyboard()


@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(
        text=hello_text,
        reply_markup=kb.start_kb()
    )

@router.message(Command("curs"))
async def cmd_start(message: Message):
    print(message)
    if message.from_user.id != 1920364845:
        return
    try:
        curs = message.text.split()[1]
        float(curs)
        db.set_curs(float(curs))
        await message.answer(f'Курс успешно обновлен на {curs}')
    except:
        await message.answer('Что-то пошло не так')

