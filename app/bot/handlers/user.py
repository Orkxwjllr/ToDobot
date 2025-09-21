import logging

from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery
from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state, State, StatesGroup
from sqlalchemy.orm import Session
from app.bot.lexicon.lexicon import LEXICON
from app.bot.keyboards.menu_plu_inline import menu_kb, remove_complete_kb
from app.bot.states.states import TaskState
from app.infrastructure.dbcommands import add_task, get_tasks_dict, get_task_id, delete_task, complete_task, get_completed_tasks
from app.bot.factiory.factory import RemoveCompleteFactory

logger = logging.getLogger(__name__)

user_router = Router()

@user_router.message(CommandStart())
async def start_message(message: Message):
    await message.answer(text=LEXICON["/start"], reply_markup=menu_kb)

@user_router.message(F.text == LEXICON["new_task"])
async def new_task(message: Message, state: FSMContext):
    await state.set_state(TaskState.fill_task_title)
    await message.answer(text=LEXICON["set_titel"], reply_markup=ReplyKeyboardRemove())

@user_router.message(StateFilter(TaskState.fill_task_title))
async def set_title(message: Message, state: FSMContext):
    await state.update_data(title=message.text)
    await state.set_state(TaskState.fill_task_text)
    await message.answer(text=LEXICON["set_task"])

@user_router.message(StateFilter(TaskState.fill_task_text))
async def set_text(message: Message, state: FSMContext, session: Session):
    await state.update_data(text=message.text)
    tasks = await state.get_data()
    add_task(
        session=session,
        user_id=message.from_user.id,
        title=tasks["title"],
        task=tasks["text"],
        is_done=False
    )
    await state.clear()
    await message.answer(text=LEXICON["added_task"], reply_markup=menu_kb)

@user_router.message(F.text == LEXICON["chek_tasks"])
async def chek_task(message: Message, session: Session):
    tasks = get_tasks_dict(session=session, user_id=message.from_user.id)
    if tasks:
        tasks_id = {}
        button = ["remove", "complete"]
        for title, description in tasks.items():
            tasks_id[title] = get_task_id(session=session, title=title)
            text = f"Задача: {title}\n{description}"
            await message.answer(text=text, reply_markup=remove_complete_kb(2, tasks_id[title], *button))
    else:
        await message.answer(text=LEXICON["no_tasks"])

@user_router.callback_query(RemoveCompleteFactory.filter())
async def remove_complete_task(callback: CallbackQuery, session: Session, callback_data: RemoveCompleteFactory):
    if callback_data.rem_com == "remove":
        delete_task(session=session, task_id=int(callback_data.task_id))
        await callback.message.edit_text(text=LEXICON["deleted_task"])
    if callback_data.rem_com == "complete":
        complete_task(session=session, task_id=int(callback_data.task_id))
        await callback.message.edit_text(text=LEXICON["completed_task"])

@user_router.message(F.text==LEXICON["complete_tasks"])
async def show_completed_task(message: Message, session: Session):
    completed_taks = get_completed_tasks(session=session, user_id=message.from_user.id)
    if completed_taks:
        for title, description in completed_taks.items():
            text = f"Задача: {title}\n{description}\n\n{LEXICON["complete"]}"
            await message.answer(text=text)
    else:
        await message.answer(text=LEXICON["no_completed_tasks"])


