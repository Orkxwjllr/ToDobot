from typing import Any, Awaitable, Callable
from aiogram import BaseMiddleware
from aiogram.types import Update
from sqlalchemy.orm import Session

class DBSessionMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Update, dict[str, Any]], Awaitable[Any]],
        event: Update,
        data: dict[str, Any],
    ) -> Any:
        
        session: Session = data.get("db_session")
        if session is None:
            raise RuntimeError("db_session is missing in middleware context")
        else:
            data["session"] = session
        
        result = await handler(event, data)
        return result
