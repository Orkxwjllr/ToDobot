from aiogram.fsm.state import State, StatesGroup


class TaskState(StatesGroup):
    fill_task_title = State()
    fill_task_text = State()