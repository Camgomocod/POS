# controllers/auth_controller.py
from sqlalchemy.orm import sessionmaker
from sqlalchemy import and_
from models.base import get_db
from models.user import User, UserRole
from datetime import datetime

class AuthController:
    """Controlador para autenticación y gestión de usuarios"""
    
    def __init__(self):
        self.db = get_db()
    
    def login(self, username, password):
        """
        Autenticar usuario
        
        Returns:
            tuple: (success: bool, user: User|None, message: str)
        """
        try:
            user = self.db.query(User).filter(
                and_(
                    User.username == username,
                    User.is_active == True
                )
            ).first()
            
            if not user:
                return False, None, "Usuario no encontrado o inactivo"
            
            if not user.check_password(password):
                return False, None, "Contraseña incorrecta"
            
            # Actualizar último login
            user.last_login = datetime.now()
            self.db.commit()
            
            return True, user, "Login exitoso"
            
        except Exception as e:
            self.db.rollback()
            return False, None, f"Error en autenticación: {str(e)}"
    
    def create_user(self, username, password, full_name, email=None, role=UserRole.REGULAR):
        """
        Crear nuevo usuario
        
        Returns:
            tuple: (success: bool, user: User|None, message: str)
        """
        try:
            # Verificar si el usuario ya existe
            existing_user = self.db.query(User).filter(User.username == username).first()
            if existing_user:
                return False, None, "El nombre de usuario ya existe"
            
            # Verificar email si se proporciona
            if email:
                existing_email = self.db.query(User).filter(User.email == email).first()
                if existing_email:
                    return False, None, "El email ya está registrado"
            
            # Crear nuevo usuario
            user = User(
                username=username,
                password=password,
                full_name=full_name,
                email=email,
                role=role
            )
            
            self.db.add(user)
            self.db.commit()
            self.db.refresh(user)
            
            return True, user, "Usuario creado exitosamente"
            
        except Exception as e:
            self.db.rollback()
            return False, None, f"Error al crear usuario: {str(e)}"
    
    def get_all_users(self):
        """Obtener todos los usuarios"""
        try:
            return self.db.query(User).order_by(User.created_at.desc()).all()
        except Exception:
            return []
    
    def get_user_by_id(self, user_id):
        """Obtener usuario por ID"""
        try:
            return self.db.query(User).filter(User.id == user_id).first()
        except Exception:
            return None
    
    def update_user(self, user_id, **kwargs):
        """Actualizar datos de usuario"""
        try:
            user = self.get_user_by_id(user_id)
            if not user:
                return False, "Usuario no encontrado"
            
            for key, value in kwargs.items():
                if key == 'password':
                    user.set_password(value)
                elif hasattr(user, key):
                    setattr(user, key, value)
            
            self.db.commit()
            return True, "Usuario actualizado exitosamente"
            
        except Exception as e:
            self.db.rollback()
            return False, f"Error al actualizar usuario: {str(e)}"
    
    def deactivate_user(self, user_id):
        """Desactivar usuario"""
        try:
            user = self.get_user_by_id(user_id)
            if not user:
                return False, "Usuario no encontrado"
            
            user.is_active = False
            self.db.commit()
            return True, "Usuario desactivado exitosamente"
            
        except Exception as e:
            self.db.rollback()
            return False, f"Error al desactivar usuario: {str(e)}"
    
    def activate_user(self, user_id):
        """Activar usuario"""
        try:
            user = self.get_user_by_id(user_id)
            if not user:
                return False, "Usuario no encontrado"
            
            user.is_active = True
            self.db.commit()
            return True, "Usuario activado exitosamente"
            
        except Exception as e:
            self.db.rollback()
            return False, f"Error al activar usuario: {str(e)}"
    
    def close(self):
        """Cerrar conexión a la base de datos"""
        if self.db:
            self.db.close()
    
    def __del__(self):
        """Destructor para cerrar la conexión"""
        self.close()
