from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from app.bot.lexicon.lexicon import LEXICON
from aiogram.utils.keyboard import InlineKeyboardBuilder
from app.bot.factiory.factory import RemoveCompleteFactory


button_1 = KeyboardButton(text=LEXICON["new_task"])
button_2 = KeyboardButton(text=LEXICON["chek_tasks"])
button_3 = KeyboardButton(text=LEXICON["complete_tasks"])

menu_kb = ReplyKeyboardMarkup(
    keyboard=[[button_2, button_3],[button_1]],
    resize_keyboard=True,
)



def remove_complete_kb(
    width: int,
    task_id: str,
    *args: str,
    **kwargs: str
) -> InlineKeyboardMarkup:

    # Инициализируем билдер
    kb_builder = InlineKeyboardBuilder()
    # Инициализируем список для кнопок
    buttons: list[InlineKeyboardButton] = []

    # Заполняем список кнопками из аргументов args и kwargs
    if args:
        for button in args:
            buttons.append(InlineKeyboardButton(
                text=LEXICON[button] if button in LEXICON else button,
                callback_data=RemoveCompleteFactory(rem_com=button, task_id=task_id).pack()))
    if kwargs:
        for button, text in kwargs.items():
            buttons.append(InlineKeyboardButton(
                text=text,
                callback_data=RemoveCompleteFactory(rem_com=button, task_id=task_id).pack()))

    # Распаковываем список с кнопками в билдер методом `row` c параметром `width`
    kb_builder.row(*buttons, width=width)

    # Возвращаем объект инлайн-клавиатуры
    return kb_builder.as_markup()