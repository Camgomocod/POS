"""
Configuraciones específicas para Windows 11
Manejo de compatibilidad para PyQtGraph y PyQt5
"""

import os
import sys

def apply_windows11_config():
    """Aplicar configuraciones específicas para Windows 11"""
    
    # Solo aplicar en Windows
    if os.name != 'nt':
        return
    
    # Configuraciones de Qt
    qt_configs = {
        'QT_QPA_PLATFORM': 'windows',
        'QT_AUTO_SCREEN_SCALE_FACTOR': '1',
        'QT_SCALE_FACTOR': '1',
        'QT_OPENGL': 'software',
        'QT_QUICK_BACKEND': 'software',
        'QT_ANGLE_PLATFORM': 'software',
        'QT_LOGGING_RULES': '*.debug=false;qt.qpa.*.debug=false'
    }
    
    # Configuraciones de PyQtGraph
    pyqtgraph_configs = {
        'PYQTGRAPH_QT_LIB': 'PyQt5',
        'PYQTGRAPH_USE_OPENGL': 'False'
    }
    
    # Aplicar configuraciones
    for key, value in {**qt_configs, **pyqtgraph_configs}.items():
        os.environ[key] = value
    
    print("✅ Configuraciones Windows 11 aplicadas")

def get_safe_pyqtgraph_config():
    """Obtener configuración segura para PyQtGraph"""
    return {
        'background': 'w',           # Fondo blanco
        'foreground': 'k',           # Texto negro
        'antialias': True,           # Antialiasing
        'useOpenGL': False,          # Sin OpenGL en Windows 11
        'enableExperimental': False, # Sin características experimentales
        'leftButtonPan': False,      # Desactivar pan con botón izquierdo
        'autoRange': True,           # Auto rango activado
        'clipToView': True,          # Recortar a vista
        'alphaBlending': True,       # Blending alfa
        'useCupy': False,            # No usar CuPy
        'useNumba': False            # No usar Numba
    }

def is_windows11():
    """Verificar si estamos en Windows 11"""
    if os.name != 'nt':
        return False
    
    try:
        import platform
        version = platform.version()
        # Windows 11 tiene versión build >= 22000
        if hasattr(platform, 'win32_ver'):
            build = platform.win32_ver()[1]
            return int(build.split('.')[-1]) >= 22000
    except:
        pass
    
    return True  # Asumir Windows 11 por defecto si no se puede determinar

# Aplicar configuraciones automáticamente al importar
if __name__ != "__main__":
    apply_windows11_config()
