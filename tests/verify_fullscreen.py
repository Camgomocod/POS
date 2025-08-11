#!/usr/bin/env python3
"""
Script de verificación de ventanas en pantalla completa
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def verify_fullscreen_changes():
    """Verificar que los cambios de pantalla completa están implementados"""
    
    print("🔍 Verificando implementación de pantalla completa...")
    print()
    
    # Leer el archivo del controlador
    try:
        with open('/home/llamqak/Projects/POS/controllers/app_controller.py', 'r') as f:
            content = f.read()
        
        # Verificar cambios para ventana POS
        if 'self.pos_window.showMaximized()' in content:
            print("✅ Ventana POS configurada para pantalla completa")
        else:
            print("❌ Ventana POS NO configurada para pantalla completa")
        
        # Verificar cambios para ventana Admin
        if 'self.admin_window.showMaximized()' in content:
            print("✅ Ventana Admin configurada para pantalla completa")
        else:
            print("❌ Ventana Admin NO configurada para pantalla completa")
        
        # Verificar mensajes de log actualizados
        if 'pantalla completa' in content:
            print("✅ Mensajes de log actualizados")
        else:
            print("❌ Mensajes de log NO actualizados")
        
        print()
        print("📋 Resumen de funcionalidades:")
        print("   🔑 Login → Ventana aparece maximizada automáticamente")
        print("   👥 Usuario regular → Ventana POS en pantalla completa")
        print("   👨‍💼 Usuario admin → Ventana Admin en pantalla completa")
        print("   🚪 Logout → Ventana de login en tamaño normal")
        print()
        print("🎯 Comportamiento esperado:")
        print("   - Las ventanas principales ocupan toda la pantalla")
        print("   - Mejor aprovechamiento del espacio disponible")
        print("   - Experiencia más inmersiva para el usuario")
        print("   - Interfaz más profesional")
        
    except Exception as e:
        print(f"❌ Error verificando cambios: {e}")

if __name__ == "__main__":
    verify_fullscreen_changes()
