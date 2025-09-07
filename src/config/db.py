import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Carga las variables de entorno desde el archivo .env
load_dotenv(dotenv_path="./.env")

# Obtiene la URL de la base de datos de las variables de entorno
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("La variable de entorno 'DATABASE_URL' no está definida.")

# Crea la instancia del motor de la base de datos
engine = create_async_engine(DATABASE_URL)

# Crea la sesión de la base de datos
# Crea la sesión de la base de datos asíncrona
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


def get_db():
    """
    Función de dependencia para obtener una sesión de la base de datos.
    Cierra la sesión después de su uso.
    """
    db = AsyncSessionLocal()
    try:
        yield db
    finally:
        db.close()
