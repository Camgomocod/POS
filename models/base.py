from sqlalchemy import create_engine, event
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
import os

# Configuración de la base de datos
DATABASE_URL = "sqlite:///data/pos.db"

# Crear directorio data si no existe
os.makedirs("data", exist_ok=True)

# Configurar SQLAlchemy con configuraciones específicas para SQLite
engine = create_engine(
    DATABASE_URL, 
    echo=False,
    poolclass=StaticPool,
    connect_args={
        "check_same_thread": False,
        # Configurar SQLite para mejor manejo de decimales
        "isolation_level": None
    }
)

# Configurar eventos para SQLite
@event.listens_for(engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    """Configurar pragmas de SQLite para mejor rendimiento y consistencia"""
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.execute("PRAGMA journal_mode=WAL")
    cursor.close()

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
