from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Configuración de la base de datos
DATABASE_URL = "sqlite:///data/pos.db"

# Crear directorio data si no existe
os.makedirs("data", exist_ok=True)

# Configurar SQLAlchemy
engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    """Obtener sesión de base de datos"""
    db = SessionLocal()
    try:
        return db
    except Exception:
        db.close()
        raise

def create_tables():
    """Crear todas las tablas"""
    Base.metadata.create_all(bind=engine)
