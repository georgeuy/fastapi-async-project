from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.todo import Base
from src.schemas import todo as schemas
from src.config.db import get_db, engine
from src.services import todo as services

# Crea la instancia de la aplicación FastAPI
# Crea la instancia de la aplicación FastAPI
app = FastAPI(
    title="Todo App API",
    description="Una API simple para gestionar una lista de tareas (todos) con FastAPI y PostgreSQL.",
    version="1.0.0",
)


# Se ejecuta al iniciar la aplicación para crear las tablas en la base de datos
@app.on_event("startup")
async def on_startup():
    print("Creando tablas de la base de datos...")
    # Usa un contexto asíncrono para crear las tablas
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Tablas creadas exitosamente.")


@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Bienvenido a la API de la lista de tareas."}


# Rutas de la API para las tareas
# Se agrega 'async' a cada función de ruta
@app.post(
    "/todos/",
    response_model=schemas.TodoResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Todos"],
)
async def create_todo_item(
    todo: schemas.TodoCreate, db: AsyncSession = Depends(get_db)
):
    return await services.create_todo(db=db, todo=todo)


@app.get("/todos/", response_model=list[schemas.TodoResponse], tags=["Todos"])
async def read_todos(
    skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)
):
    todos = await services.get_todos(db, skip=skip, limit=limit)
    return todos


@app.get("/todos/{todo_id}", response_model=schemas.TodoResponse, tags=["Todos"])
async def read_todo_by_id(todo_id: int, db: AsyncSession = Depends(get_db)):
    db_todo = await services.get_todo_by_id(db, todo_id)
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    return db_todo


@app.put("/todos/{todo_id}", response_model=schemas.TodoResponse, tags=["Todos"])
async def update_todo_item(
    todo_id: int,
    todo: schemas.TodoCreate,
    completed: bool | None = None,
    db: AsyncSession = Depends(get_db),
):
    db_todo = await services.update_todo(
        db, todo_id=todo_id, todo=todo, completed=completed
    )
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    return db_todo


@app.delete("/todos/{todo_id}", response_model=schemas.TodoResponse, tags=["Todos"])
async def delete_todo_item(todo_id: int, db: AsyncSession = Depends(get_db)):
    db_todo = await services.delete_todo(db, todo_id=todo_id)
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    return db_todo
