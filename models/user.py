# models/user.py
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Enum
from sqlalchemy.sql import func
from models.base import Base
import enum
import hashlib
import secrets

class UserRole(enum.Enum):
    """Roles de usuario"""
    ADMIN = "admin"
    REGULAR = "regular"

class User(Base):
    """Modelo de usuario con roles y autenticación"""
    
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=True)
    password_hash = Column(String(255), nullable=False)
    salt = Column(String(255), nullable=False)
    role = Column(Enum(UserRole), default=UserRole.REGULAR, nullable=False)
    full_name = Column(String(100), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    last_login = Column(DateTime(timezone=True), nullable=True)
    
    def __init__(self, username, password, full_name, email=None, role=UserRole.REGULAR):
        self.username = username
        self.full_name = full_name
        self.email = email
        self.role = role
        self.salt = secrets.token_hex(32)
        self.password_hash = self._hash_password(password)
    
    def _hash_password(self, password):
        """Crear hash seguro de la contraseña"""
        return hashlib.pbkdf2_hmac('sha256', 
                                 password.encode('utf-8'), 
                                 self.salt.encode('utf-8'), 
                                 100000).hex()
    
    def check_password(self, password):
        """Verificar contraseña"""
        return self.password_hash == self._hash_password(password)
    
    def set_password(self, password):
        """Cambiar contraseña"""
        self.salt = secrets.token_hex(32)
        self.password_hash = self._hash_password(password)
    
    @property
    def is_admin(self):
        """Verificar si es administrador"""
        return self.role == UserRole.ADMIN
    
    @property
    def role_display(self):
        """Mostrar rol en formato legible"""
        return "Administrador" if self.is_admin else "Usuario Regular"
    
    def __repr__(self):
        return f"<User(username='{self.username}', role='{self.role.value}', active={self.is_active})>"
