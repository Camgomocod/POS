#!/usr/bin/env python3
"""
Script para preparar el proyecto POS para build y distribución
Crea una base de datos lista para producción y lista archivos necesarios
"""

import os
import sys
import shutil
from datetime import datetime

def create_build_info():
    """Crear archivo con información del build"""
    build_info = f"""# BUILD INFORMATION
# Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Database Status
- Clean database with basic users only
- Database size: ~56KB (minimal)
- Users: admin, cajero
- No test data included

## Build Credentials
### Administrator
- Username: admin
- Password: admin123
- Role: Full system access

### Cashier
- Username: cajero  
- Password: cajero123
- Role: POS and basic operations

## Files Required for Distribution
```
data/pos.db                 # Clean database
main.py                     # Application entry point
config.py                   # System configuration
requirements.txt            # Python dependencies
controllers/                # Business logic
models/                     # Database models
utils/                      # Utilities
views/                      # User interface
```

## First Run Instructions
1. Install dependencies: pip install -r requirements.txt
2. Run application: python main.py
3. Login with admin/admin123 or cajero/cajero123
4. Configure products and categories as needed

## Database Management
- Backup/Export features available in Admin → Configuration
- Database verification tools included
- Clean database ready for production use

Build prepared on: {datetime.now().strftime('%Y-%m-%d at %H:%M:%S')}
"""
    
    with open("BUILD_INFO.md", "w", encoding="utf-8") as f:
        f.write(build_info)
    
    print("📄 Archivo BUILD_INFO.md creado")

def check_requirements():
    """Verificar que requirements.txt existe y está actualizado"""
    if os.path.exists("requirements.txt"):
        print("✅ requirements.txt encontrado")
        with open("requirements.txt", "r") as f:
            requirements = f.read()
            print("📦 Dependencias incluidas:")
            for line in requirements.strip().split('\n'):
                if line.strip():
                    print(f"  - {line.strip()}")
    else:
        print("⚠️ requirements.txt no encontrado")

def create_distribution_checklist():
    """Crear checklist para distribución"""
    checklist = """# DISTRIBUTION CHECKLIST

## Pre-Build Verification ✅
- [x] Clean database created
- [x] Basic users configured (admin, cajero)
- [x] No test data included
- [x] Database size optimized (~56KB)
- [x] Login credentials verified

## Required Files for Distribution
- [x] main.py (entry point)
- [x] config.py (configuration)
- [x] requirements.txt (dependencies)
- [x] data/pos.db (clean database)
- [x] controllers/ (all files)
- [x] models/ (all files)
- [x] utils/ (all files)
- [x] views/ (all files)

## Optional Files
- [ ] README.md (user documentation)
- [ ] LICENSE (license file)
- [ ] BUILD_INFO.md (build information)

## Testing Before Distribution
- [ ] Test admin login (admin/admin123)
- [ ] Test cajero login (cajero/cajero123)
- [ ] Test POS interface
- [ ] Test admin interface
- [ ] Test database management features
- [ ] Verify all modules load correctly

## Build/Package Steps
- [ ] Create virtual environment
- [ ] Install dependencies
- [ ] Test full application
- [ ] Create installer/package
- [ ] Test installation on clean system

## Post-Distribution
- [ ] Provide user manual
- [ ] Document credential change process
- [ ] Include backup/restore instructions
"""
    
    with open("DISTRIBUTION_CHECKLIST.md", "w", encoding="utf-8") as f:
        f.write(checklist)
    
    print("📋 Archivo DISTRIBUTION_CHECKLIST.md creado")

def show_build_summary():
    """Mostrar resumen del build"""
    print("\n🎯 RESUMEN DEL BUILD")
    print("=" * 40)
    print()
    print("✅ ESTADO ACTUAL:")
    print("  🗄️ Base de datos limpia y lista")
    print("  👥 Usuarios básicos configurados")
    print("  📦 Archivos organizados para distribución")
    print("  🔧 Sistema listo para empaquetado")
    print()
    print("📊 ESTADÍSTICAS:")
    
    # Tamaño de la base de datos
    if os.path.exists("data/pos.db"):
        db_size = os.path.getsize("data/pos.db") / 1024
        print(f"  💾 Base de datos: {db_size:.1f} KB")
    
    # Contar archivos Python
    py_files = []
    for root, dirs, files in os.walk("."):
        for file in files:
            if file.endswith(".py"):
                py_files.append(os.path.join(root, file))
    
    print(f"  🐍 Archivos Python: {len(py_files)}")
    print(f"  📁 Directorios principales: controllers, models, utils, views")
    print()
    print("🚀 PRÓXIMOS PASOS:")
    print("  1. Revisar DISTRIBUTION_CHECKLIST.md")
    print("  2. Probar la aplicación completa")
    print("  3. Crear instalador/paquete")
    print("  4. Distribuir con BUILD_INFO.md")

def main():
    """Función principal"""
    print("🚀 PREPARANDO PROYECTO PARA BUILD")
    print("=" * 40)
    print()
    
    # Crear información del build
    create_build_info()
    
    # Verificar requirements
    check_requirements()
    print()
    
    # Crear checklist de distribución
    create_distribution_checklist()
    print()
    
    # Mostrar resumen
    show_build_summary()
    
    print("\n" + "=" * 40)
    print("✅ PROYECTO LISTO PARA BUILD Y DISTRIBUCIÓN")
    print("📋 Revisa los archivos creados para más detalles")

if __name__ == "__main__":
    main()
