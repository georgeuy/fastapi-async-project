from sqlalchemy import select
from sqlalchemy.orm import Session
from src.models import todo as models
from src.schemas import todo as schemas


async def get_todos(db: Session, skip: int = 0, limit: int = 100):
    """
    Obtiene todas las tareas de la base de datos con paginación de forma asíncrona.
    """
    result = await db.execute(select(models.Todo).offset(skip).limit(limit))
    return result.scalars().all()


async def create_todo(db: Session, todo: schemas.TodoCreate):
    """
    Crea una nueva tarea en la base de datos de forma asíncrona.
    """
    db_todo = models.Todo(title=todo.title, description=todo.description)
    db.add(db_todo)
    await db.commit()
    await db.refresh(db_todo)
    return db_todo


async def get_todo_by_id(db: Session, todo_id: int):
    """
    Obtiene una tarea por su ID de forma asíncrona.
    """
    result = await db.execute(select(models.Todo).filter(models.Todo.id == todo_id))
    return result.scalar_one_or_none()


async def update_todo(
    db: Session, todo_id: int, todo: schemas.TodoCreate, completed: bool | None = None
):
    """
    Actualiza una tarea existente de forma asíncrona.
    """
    db_todo = await get_todo_by_id(db, todo_id)
    if db_todo:
        db_todo.title = todo.title
        db_todo.description = todo.description
        if completed is not None:
            db_todo.completed = completed
        await db.commit()
        await db.refresh(db_todo)
    return db_todo


async def delete_todo(db: Session, todo_id: int):
    """
    Elimina una tarea por su ID de forma asíncrona.
    """
    db_todo = await get_todo_by_id(db, todo_id)
    if db_todo:
        await db.delete(db_todo)
        await db.commit()
    return db_todo
