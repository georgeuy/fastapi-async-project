from pydantic import BaseModel

class TodoBase(BaseModel):
    """
    Esquema base para la creación y actualización de una tarea.
    """
    title: str
    description: str | None = None

class TodoCreate(TodoBase):
    """
    Esquema para la creación de una tarea.
    """
    pass

class TodoResponse(TodoBase):
    """
    Esquema para la respuesta de la API.
    Incluye el ID y el estado 'completed' de la tarea.
    """
    id: int
    completed: bool

    class Config:
        # Permite que la respuesta se cree a partir de una instancia del modelo ORM
        from_attributes = True
