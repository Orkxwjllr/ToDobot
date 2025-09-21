from aiogram.filters.callback_data import CallbackData


class RemoveCompleteFactory(CallbackData, prefix='any'):
    rem_com: str
    task_id: int