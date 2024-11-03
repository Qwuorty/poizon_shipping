from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import datetime as dt
from random import randint
from callbacks import *
import sqlite3


class Keyboard:
    def __init__(self):
        pass

    def start_kb(self):
        builder = InlineKeyboardBuilder()
        builder.button(text='Мы в ТГ', url='https://t.me/poizonshippin')
        builder.button(text='Мы в ВК', url='https://vk.com/pznshippin')
        builder.button(text='Сделать заказ', callback_data='start_all')
        builder.adjust(2, 1)
        return builder.as_markup(resize_keyboard=1)

    def main_kb(self):
        builder = InlineKeyboardBuilder()
        builder.button(text='Оформить заказ', callback_data='make_offer')
        builder.button(text='Рассчитать стоимость', callback_data='count_offer')
        builder.button(text='Скачать приложение пойзон', callback_data='apps')
        builder.button(text='FAQ', callback_data='faq')
        builder.button(text='Доставка', callback_data='deliv')
        builder.button(text='Как оформить заказ', callback_data='how_to')
        builder.button(text='Cвязаться с менеджером', callback_data='connect')
        builder.adjust(1)
        return builder.as_markup(resize_keyboard=1)

    def stop_talk(self, chat_id):
        builder = InlineKeyboardBuilder()
        builder.button(text='Закрыть вопрос', callback_data=f'close_{chat_id}')
        return builder.as_markup()

    def get_last_kb(self):
        builder = InlineKeyboardBuilder()
        builder.button(text='Редактировать заявку', callback_data='red_offfer')
        builder.button(text='Оформить заказ', callback_data='send_offfer')
        builder.adjust(1)
        return builder.as_markup()

    def red_kb(self):
        builder = InlineKeyboardBuilder()
        builder.button(text='Размер', callback_data='red_size')
        builder.button(text='Ссылка', callback_data='red_link')
        builder.button(text='Стоимость', callback_data='red_cost')
        builder.button(text='Тип доставки', callback_data='red_dost')
        builder.button(text='🔙', callback_data='back_menu')
        builder.adjust(1)
        return builder.as_markup()

    def how_to_kb(self, ind):
        builder = InlineKeyboardBuilder()
        if ind == 0:
            builder.button(text='android', url='https://wap.25pp.com/xiazai/6696712/history_v727/')
            builder.button(text='ios', url='https://apps.apple.com/app/id1012871328')
            builder.button(text='Cвязаться с менеджером', callback_data='connect')
            builder.button(text='→', callback_data='how_to_1')
            builder.button(text='Меню', callback_data='start_all')
            builder.adjust(2, 1, 2)
        elif ind == 8:
            builder.button(text='←', callback_data='how_to_6')
            builder.button(text='Меню', callback_data='start_all')
            builder.button(text='Cвязаться с менеджером', callback_data='connect')
            builder.button(text='Оформить заказ', callback_data='make_offer')
            builder.adjust(2, 1,1)
        else:
            builder.button(text='←', callback_data=f'how_to_{ind - 1}')
            builder.button(text='→', callback_data=f'how_to_{ind + 1}')
            builder.button(text='Меню', callback_data='start_all')
            builder.adjust(2, 1)
        return builder.as_markup()

    def delivery(self):
        builder = InlineKeyboardBuilder()
        builder.button(text='Обычная', callback_data='dev_1')
        builder.button(text='Экспресс', callback_data='dev_2')
        builder.button(text='🔙', callback_data='start_all')
        builder.adjust(2, 1)
        return builder.as_markup()

    def make(self):
        builder = InlineKeyboardBuilder()
        builder.button(text='Сделать заказ', callback_data='asdasdasd')
        builder.button(text='🔙', callback_data='start_all')
        builder.adjust(1)
        return builder.as_markup(resize_keyboard=1)

    def back(self):
        builder = InlineKeyboardBuilder()
        builder.button(text='🔙', callback_data='start_all')
        builder.adjust(1)
        return builder.as_markup(resize_keyboard=1)

    def back_and_admin(self):
        builder = InlineKeyboardBuilder()
        builder.button(text='🔙', callback_data='start_all')
        builder.button(text='Cвязаться с менеджером', callback_data='connect')
        builder.adjust(2)
        return builder.as_markup(resize_keyboard=1)

    def apps(self):
        builder = InlineKeyboardBuilder()
        builder.button(text='android', url='https://wap.25pp.com/xiazai/6696712/history_v727/')
        builder.button(text='ios', url='https://apps.apple.com/app/id1012871328')
        builder.button(text='🔙', callback_data='start_all')
        builder.adjust(1)
        return builder.as_markup(resize_keyboard=1)

    def faq(self):
        builder = InlineKeyboardBuilder()
        builder.button(text='Cвязаться с менеджером', callback_data='connect')
        builder.button(text='🔙', callback_data='start_all')
        builder.adjust(1)
        return builder.as_markup()


kb = Keyboard()
