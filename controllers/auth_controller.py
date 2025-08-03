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
            # Ensure session returns fresh data after updates
            self.db.expire_all()
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
    
    def validate_user_data(self, username, email=None, user_id=None):
        """
        Validar datos de usuario para evitar duplicados
        
        Args:
            username: Nombre de usuario a validar
            email: Email a validar (opcional)
            user_id: ID del usuario en caso de edición (para excluirlo de la validación)
            
        Returns:
            tuple: (is_valid: bool, message: str)
        """
        try:
            # Validar username
            username_query = self.db.query(User).filter(User.username == username)
            if user_id:
                username_query = username_query.filter(User.id != user_id)
            
            if username_query.first():
                return False, "El nombre de usuario ya existe"
            
            # Validar email si se proporciona
            if email:
                email_query = self.db.query(User).filter(User.email == email)
                if user_id:
                    email_query = email_query.filter(User.id != user_id)
                
                if email_query.first():
                    return False, "El email ya está registrado"
            
            return True, "Datos válidos"
            
        except Exception as e:
            return False, f"Error en validación: {str(e)}"
    
    def get_user_stats(self):
        """
        Obtener estadísticas de usuarios
        
        Returns:
            dict: Diccionario con estadísticas
        """
        try:
            users = self.get_all_users()
            
            total_users = len(users)
            active_users = len([u for u in users if u.is_active])
            inactive_users = total_users - active_users
            admin_users = len([u for u in users if u.role == UserRole.ADMIN])
            regular_users = len([u for u in users if u.role == UserRole.REGULAR])
            
            # Usuarios con login reciente (últimos 7 días)
            from datetime import datetime, timedelta
            week_ago = datetime.now() - timedelta(days=7)
            recent_logins = len([u for u in users if u.last_login and u.last_login >= week_ago])
            
            return {
                'total_users': total_users,
                'active_users': active_users,
                'inactive_users': inactive_users,
                'admin_users': admin_users,
                'regular_users': regular_users,
                'recent_logins': recent_logins
            }
            
        except Exception:
            return {
                'total_users': 0,
                'active_users': 0,
                'inactive_users': 0,
                'admin_users': 0,
                'regular_users': 0,
                'recent_logins': 0
            }
    
    def close(self):
        """Cerrar conexión a la base de datos"""
        if self.db:
            self.db.close()
    
    def __del__(self):
        """Destructor para cerrar la conexión"""
        self.close()
