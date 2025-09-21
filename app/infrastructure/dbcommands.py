from sqlalchemy.orm import Session
from app.infrastructure.models.model import TaskBase

def add_task(
    session: Session,
    user_id: int,
    title: str,
    task: str,
    is_done: bool = False
) -> TaskBase:
    new_task = TaskBase(
        user_id=user_id,
        title=title,
        task=task,
        is_done=is_done
    )
    session.add(new_task)
    session.commit()
    session.refresh(new_task)
    return new_task

def get_tasks_dict(session: Session, user_id: int | None = None) -> dict[str, str]:
    query = session.query(TaskBase).filter(TaskBase.is_done == False)

    if user_id is not None:
        query = query.filter(TaskBase.user_id == user_id)

    tasks = query.all()
    return {task.title: task.task for task in tasks}

def delete_task(session: Session, task_id: int) -> bool:
    task = session.get(TaskBase, task_id)
    if task:
        session.delete(task)
        session.commit()
        return True
    return False

def get_task_id(session: Session, title: str) -> int | None:
    task = session.query(TaskBase).filter(TaskBase.title == title).first()
    return task.id if task else None

def complete_task(session: Session, task_id: int) -> bool:
    task = session.query(TaskBase).filter(TaskBase.id == task_id).first()
    if task:
        task.is_done = True
        session.commit()
        return True
    return False

def get_completed_tasks(session: Session, user_id: int | None = None) -> dict[str, str]:
    query = session.query(TaskBase).filter(TaskBase.is_done == True)

    if user_id is not None:
        query = query.filter(TaskBase.user_id == user_id)

    tasks = query.all()
    return {task.title: task.task for task in tasks}