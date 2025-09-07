from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base

# Define la base declarativa para los modelos ORM
Base = declarative_base()

class Todo(Base):
    """
    Modelo de la tabla 'todos' en la base de datos.
    Representa una tarea de la lista.
    """
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    completed = Column(Boolean, default=False)