import time

from aiogram import Router, F, types
from aiogram.filters import Command, StateFilter
from aiogram.types import Message, ReplyKeyboardRemove, input_file, InputMediaPhoto, InputMediaVideo, CallbackQuery
from aiogram.types.input_file import FSInputFile
from aiogram.utils.media_group import MediaGroupBuilder

from keyboards import keyboard
from callbacks import Curs, Back, FAQ, FindOffer, MakeOffer, Calc
from db import db
from aiogram.fsm.context import FSMContext
from texts import how_to_make_offer_text, hello_text, how_to_text
from texts import bot2, faq_text
import datetime as dt

admin_id = 5913060173
router = Router()
kb = keyboard.Keyboard()


@router.callback_query(F.data == 'make_offer')
async def start_all(call: CallbackQuery, state: FSMContext):
    await call.message.delete()
    await call.message.answer('''Прикрепите ссылку на товар, который вам нужен.
Если у вас есть сложности с ее получением, узнайте больше в нашем FAQ или нажмите кнопку для вызова менеджера''',
                              reply_markup=kb.back_and_admin())
    db.add_user(call.from_user.id)
    await state.set_state('wait_link')



@router.callback_query(F.data == 'start_all')
async def start_all(call: CallbackQuery, state: FSMContext):
    await state.clear()
    if call.message.caption:
        await call.message.edit_media(media=InputMediaPhoto(media=FSInputFile(f"media/main.jpg")),
                                      reply_markup=kb.main_kb())
    else:
        await call.message.delete()
        await call.message.answer_photo(photo=FSInputFile(f"media/main.jpg"), reply_markup=kb.main_kb())


@router.callback_query(F.data == 'connect')
async def start_all(call: CallbackQuery, state: FSMContext):
    if db.open_connect():
        db.add_talk(call.from_user.id, txt=f'Пользователь хочет, чтобы вы с ним связались\n @{call.from_user.username}')
        await bot2.send_message(admin_id, 'Новый запрос в очереди')
        await call.message.answer(f"""Связываем вас с менеджером. Вам ответят в порядке очереди. Спасибо за ожидание!""")
    else:
        db.add_talk(call.from_user.id, txt=f'Пользователь хочет, чтобы вы с ним связались\n@{call.from_user.username}')
        await call.message.answer('Связываем вас с менеджером. Вам ответят в порядке очереди. Спасибо за ожидание!')
        txt2 = f'Вы общаетесь с пользователем @{call.from_user.username}'
        message = await bot2.send_message(admin_id, txt2, reply_markup=kb.stop_talk(call.from_user.id))
        await state.set_state('talking')
        await bot2.pin_chat_message(admin_id, message.message_id)
    await call.answer()



@router.callback_query(F.data == 'send_offfer')
async def start_all(call: CallbackQuery, state: FSMContext):
    txt = f'Вы общаетесь с пользователем @{call.from_user.username}\n' + db.get_text(call.from_user.id)
    await call.message.delete()
    if db.open_connect():
        db.add_talk(call.from_user.id, txt=txt)
        await bot2.send_message(admin_id, 'Новый запрос в очереди')
        await call.message.answer(
            f"""“Спасибо за ваш заказ! Наш менеджер вернется с деталями в ближайшее время. Если вам не ответили в течение 2 часов – дарим скидку 15%""",reply_markup=kb.back())
    else:
        await call.message.answer(
            f"""“Спасибо за ваш заказ! Наш менеджер вернется с деталями в ближайшее время. Если вам не ответили в течение 2 часов – дарим скидку 15%""",
            reply_markup=kb.back())
        db.add_talk(call.from_user.id, txt=txt)
        message = await bot2.send_message(admin_id, txt, reply_markup=kb.stop_talk(call.from_user.id))
        await state.set_state('talking')
        await bot2.pin_chat_message(admin_id, message.message_id)
    await call.answer()

@router.message(StateFilter('talking'))
async def last_caaszxatcher(message: Message, state: FSMContext):
    if db.is_open(message.from_user.id):
        await message.copy_to(admin_id)


@router.callback_query(F.data == 'count_offer')
async def start_all(call: CallbackQuery, state: FSMContext):
    await call.message.delete()
    await call.message.answer(f"Укажите, пожалуйста, стоимость товара в юанях")
    await state.set_state('wait_count_offer')


@router.message(StateFilter('wait_count_offer'))
async def last_caaszxatcher(message: Message, state: FSMContext):
    curs = db.get_curs()
    try:
        await message.answer(f"Стоимость вашего товара - {int(float(curs) * int(message.text) + 1000)} рублей")
        time.sleep(2)
        await message.answer_photo(photo=FSInputFile(f"media/main.jpg"), reply_markup=kb.main_kb())
    except:
        await message.answer(F"Упс, кажется что-то пошло не так")
        await message.answer_photo(photo=FSInputFile(f"media/main.jpg"), reply_markup=kb.main_kb())
    await state.clear()





@router.callback_query(F.data == 'deliv')
async def start_all(call: CallbackQuery):
    try:
        await call.message.edit_text('''Мы доставим ваш заказ в срок от 10 до 20 дней. Быстрее вы не найдете нигде.Доставляем с помощью СДЭК, Почты России.Весь процесс перемещения товара мы предоставляем по вашему запросу. Сумма доставки может быть разная, но варьируется от 600 до 1500 рублей. Ее нужно уточнять индивидуально, поскольку она зависит от веса вашего заказа.Подробнее можете прочитать в нашей статье!
https://telegra.ph/FAQ-10-30-14''', reply_markup=kb.back())
    except:
        await call.message.edit_caption(caption='''Мы доставим ваш заказ в срок от 10 до 20 дней. Быстрее вы не найдете нигде.Доставляем с помощью СДЭК, Почты России.Весь процесс перемещения товара мы предоставляем по вашему запросу. Сумма доставки может быть разная, но варьируется от 600 до 1500 рублей. Ее нужно уточнять индивидуально, поскольку она зависит от веса вашего заказа.Подробнее можете прочитать в нашей статье!
https://telegra.ph/FAQ-10-30-14''', reply_markup=kb.back())


@router.callback_query(F.data.startswith('close'))
async def start_all(call: CallbackQuery):
    chat_id = call.data.split('_')[1]
    await bot2.unpin_all_chat_messages(admin_id)
    await call.message.delete()
    await call.answer('Диалог успешно завершен')
    await bot2.send_message(chat_id, 'Менеджер завершил диалог с вами')
    db.close_talk(chat_id)
    if db.wait_connect():
        chat_id = db.wait_connect()[0]
        db.open_new_connect(chat_id)
        txt = db.get_connect_text(chat_id)
        message = await bot2.send_message(admin_id, txt, reply_markup=kb.stop_talk(call.from_user.id))
        await bot2.send_message(chat_id, 'Менеджер зашел в диалог с вами')
        await bot2.pin_chat_message(admin_id, message.message_id)


@router.callback_query(F.data.startswith('faq'))
async def start_all(call: CallbackQuery):
    await call.message.edit_caption(
        caption='В этой статье мы собрали все ответы на частозадаваемые вопросы: https://telegra.ph/FAQ-10-30-14',
        reply_markup=kb.faq())


@router.callback_query(F.data.startswith('how_to'))
async def start_all(call: CallbackQuery):
    if call.data.count('_') == 2:
        ind = int(call.data.split('_')[2])
        if ind == 0:
            await call.message.edit_media(
                media=InputMediaPhoto(media=FSInputFile(f"media/how_to_{ind}.jpg"), caption=how_to_text[ind]),
                reply_markup=kb.how_to_kb(ind))
        else:
            await call.message.edit_media(
                media=InputMediaPhoto(media=FSInputFile(f"media/how_to_{ind}.jpg"), caption=how_to_text[ind]),
                reply_markup=kb.how_to_kb(ind))
    else:
        await call.message.edit_media(
            media=InputMediaPhoto(media=FSInputFile(f"media/how_to_{0}.jpg"), caption=how_to_text[0]),
            reply_markup=kb.how_to_kb(0))


@router.callback_query(F.data == 'apps')
async def start_all(call: CallbackQuery):
    await call.message.edit_caption(caption='Сообщение для приложений', reply_markup=kb.apps())


@router.callback_query(F.data.startswith('offer'))
async def get_send_shtrihcode(call: CallbackQuery):
    message_id = int(call.data.split('_')[1])
    await call.message.answer(f"Мы уже передали ваш запрос Администратору, в ближайшее время он с вами свяжется",
                              reply_markup=kb.start_kb())
    # admin_id = 811073879
    admin_id = 1920364845
    await bot2.send_message(chat_id=admin_id,
                            text=f"ВНИМАНИЕ, НОВЫЙ ЗАКАЗ ОТ @{call.from_user.username}\nРазмер - {db.get_size(call.from_user.id)}\nСсылка - {db.get_link(call.from_user.id)}")
    await bot2.copy_message(chat_id=admin_id, from_chat_id=call.from_user.id, message_id=message_id + 1)
    await call.answer()


@router.message(StateFilter('wait_link'))
async def last_caaszxatcher(message: Message, state: FSMContext):
    try:
        db.add_link(message.from_user.id, message.text)
        await state.set_state('wait_size')
        await message.answer(f"""Введите размер, который вам необходим.
Если у вас есть сложности с его определением, узнайте больше в нашем FAQ или нажмите кнопку для вызова менеджера""",
                             reply_markup=kb.back_and_admin())
    except:
        await message.answer(
            'Что-то пошло не так, попробуй ввести стоимость еще раз или вернитесь в меню, нажав кнопку "Назад 🔙"')


@router.message(StateFilter('wait_size'))
async def last_caaszxatcher(message: Message, state: FSMContext):
    try:
        db.add_size(message.from_user.id, message.text)
        await state.set_state('wait_price')
        await message.answer(f"""Введите стоимость товара в юанях.
Если у вас есть сложности, узнайте больше в нашем FAQ или нажмите кнопку для вызова менеджера""",reply_markup=kb.back_and_admin())
    except:
        await message.answer(
            'Что-то пошло не так, попробуй ввести стоимость еще раз или вернитесь в меню, нажав кнопку "Назад 🔙"')


@router.message(StateFilter('wait_price'))
async def last_caaszxatcher(message: Message, state: FSMContext):
    try:
        await state.clear()
        await message.answer(
            f"""Выберите удобную для вас форму доставки:
Обычная: Х рублей за килограмм. Доставим за 18-21 день
Экспресс: У рублей. Доставим за 7-10 дней
""",
            reply_markup=kb.delivery())
    except:
        await message.answer(
            'Что-то пошло не так, попробуй ввести стоимость еще раз или вернитесь в меню, нажав кнопку "Назад 🔙"')


@router.callback_query(F.data.startswith('dev'))
async def asbfdsfgh(call: CallbackQuery):
    dev_type = call.data.split('_')[1]
    dev_type = int(dev_type)
    db.add_dost(call.from_user.id, dev_type)
    txt = db.get_text(call.from_user.id)
    await call.message.delete()
    await call.message.answer(txt, reply_markup=kb.get_last_kb())


@router.callback_query(F.data.startswith('red_offfer'))
async def asbfdsfgh(call: CallbackQuery):
    txt = db.get_text(call.from_user.id)
    await call.message.edit_text(text=txt + '\n\nВыберите, что вы хотите изменить', reply_markup=kb.red_kb())


@router.callback_query(F.data.startswith('red_size'))
async def asbfdsfgh(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text(f"Введите новый размер")
    await state.set_state('wait_red_size')


@router.message(StateFilter('wait_red_size'))
async def last_caaszxatcher(message: Message, state: FSMContext):
    await state.clear()
    db.add_size(message.from_user.id, message.text)
    txt = db.get_text(message.from_user.id)
    await message.answer(txt, reply_markup=kb.get_last_kb())


@router.callback_query(F.data.startswith('red_link'))
async def asbfdsfgh(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text(f"Введите новую ссылку")
    await state.set_state('wait_red_link')


@router.message(StateFilter('wait_red_link'))
async def last_caaszxatcher(message: Message, state: FSMContext):
    await state.clear()
    db.add_link(message.from_user.id, message.text)
    txt = db.get_text(message.from_user.id)
    await message.answer(txt, reply_markup=kb.get_last_kb())


@router.callback_query(F.data.startswith('red_cost'))
async def asbfdsfgh(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text(f"Введите новую стоимость")
    await state.set_state('wait_red_cost')


@router.message(StateFilter('wait_red_cost'))
async def last_caaszxatcher(message: Message, state: FSMContext):
    await state.clear()
    try:
        db.add_cost(message.from_user.id, int(message.text))
        txt = db.get_text(message.from_user.id)
        await message.answer(txt, reply_markup=kb.get_last_kb())
    except:
        await message.answer('Что-то пошло не так')
        txt = db.get_text(message.from_user.id)
        await message.answer(txt, reply_markup=kb.get_last_kb())


@router.callback_query(F.data.startswith('red_dost'))
async def asbfdsfgh(call: CallbackQuery, state: FSMContext):
    await state.clear()
    await call.message.edit_caption(
        f"""Выберите удобную для вас форму доставки:
Обычная: Х рублей за килограмм. Доставим за 18-21 день
Экспресс: У рублей. Доставим за 7-10 дней
""",
        reply_markup=kb.delivery())


@router.callback_query(F.data.startswith('back_menu'))
async def asbfdsfgh(call: CallbackQuery):
    txt = db.get_text(call.from_user.id)
    await call.message.edit_text(txt, reply_markup=kb.get_last_kb())


@router.message()
async def admin_talk(message: Message):
    if message.from_user.id == admin_id and db.open_connect():
        await message.copy_to(db.get_open_chat_id())
    elif message.from_user.id == db.get_open_chat_id():
        await message.copy_to(admin_id)