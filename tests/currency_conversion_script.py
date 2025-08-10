#!/usr/bin/env python3
"""
Script de conversión de moneda de Soles (S/) a Pesos Colombianos ($)
Actualiza todas las referencias de moneda en el código fuente
"""

import os
import re
import shutil
from datetime import datetime

def backup_file(file_path):
    """Crear respaldo de un archivo antes de modificarlo"""
    backup_path = f"{file_path}.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    shutil.copy2(file_path, backup_path)
    print(f"Respaldo creado: {backup_path}")
    return backup_path

def convert_currency_in_file(file_path, conversions):
    """Aplicar conversiones de moneda en un archivo específico"""
    print(f"\n🔄 Procesando: {file_path}")
    
    # Crear respaldo
    backup_file(file_path)
    
    # Leer contenido
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    changes_made = 0
    
    # Aplicar conversiones
    for pattern, replacement in conversions:
        if isinstance(pattern, str):
            # Búsqueda literal
            if pattern in content:
                content = content.replace(pattern, replacement)
                changes_made += content.count(replacement) - original_content.count(replacement)
                print(f"  ✅ Reemplazado: '{pattern}' → '{replacement}'")
        else:
            # Búsqueda con regex
            matches = pattern.findall(content)
            if matches:
                content = pattern.sub(replacement, content)
                changes_made += len(matches)
                print(f"  ✅ Reemplazado patrón regex: {len(matches)} coincidencias")
    
    # Guardar si hubo cambios
    if changes_made > 0:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  📝 Archivo actualizado: {changes_made} cambios")
    else:
        print(f"  ℹ️  Sin cambios necesarios")
    
    return changes_made

def main():
    """Función principal de conversión"""
    print("🏦 CONVERSIÓN DE MONEDA: SOLES → PESOS COLOMBIANOS")
    print("=" * 60)
    
    base_path = "/home/llamqak/Projects/POS"
    total_changes = 0
    
    # Definir archivos y sus conversiones específicas
    files_to_convert = {
        "views/products_management_view.py": [
            # Convertir S/ a $ en formato de precios
            ('f"S/ {product.price:.2f}"', 'f"$ {product.price:.2f}"'),
            ('f"S/ {product.cost:.2f}"', 'f"$ {product.cost:.2f}"'),
        ],
        
        "views/payment_history_window.py": [
            # Asegurar formato consistente con comas para miles
            (re.compile(r'f"\${([^}]+):.0f}"'), r'f"$ {\1:,.0f}"'),
            (re.compile(r'f"\${([^}]+):\.0f}"'), r'f"$ {\1:,.0f}"'),
        ],
        
        "views/pos_window.py": [
            # Formato consistente con espacio después del $
            (re.compile(r'f"\${([^}]+):,\.0f}"'), r'f"$ {\1:,.0f}"'),
            (re.compile(r'f"\${([^}]+):.0f}"'), r'f"$ {\1:,.0f}"'),
            (re.compile(r'f"\${([^}]+):,\.0f}"'), r'f"$ {\1:,.0f}"'),
        ],
        
        "views/main_window.py": [
            # Asegurar formato consistente en ventana principal
            (re.compile(r'f"\${([^}]+):.2f}"'), r'f"$ {\1:,.2f}"'),
        ],
        
        "utils/printer.py": [
            # Conversiones en impresora térmica (si existen)
            ('S/', '$'),
            (re.compile(r'S/\s*\{'), '$ {'),
        ]
    }
    
    # Procesar cada archivo
    for relative_path, conversions in files_to_convert.items():
        file_path = os.path.join(base_path, relative_path)
        
        if os.path.exists(file_path):
            changes = convert_currency_in_file(file_path, conversions)
            total_changes += changes
        else:
            print(f"⚠️  Archivo no encontrado: {file_path}")
    
    # Buscar y convertir cualquier referencia restante de "S/"
    print(f"\n🔍 Buscando referencias adicionales de 'S/'...")
    
    views_path = os.path.join(base_path, "views")
    for filename in os.listdir(views_path):
        if filename.endswith('.py'):
            file_path = os.path.join(views_path, filename)
            
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Buscar patrones de S/ que no hayamos convertido
            if 'S/' in content and filename not in [f.split('/')[-1] for f in files_to_convert.keys()]:
                print(f"  📋 Referencia de S/ encontrada en: {filename}")
                
                # Conversión general de S/ a $
                general_conversions = [
                    ('S/', '$'),
                    ('"S/ "', '"$ "'),
                    ("'S/ '", "'$ '"),
                ]
                
                changes = convert_currency_in_file(file_path, general_conversions)
                total_changes += changes
    
    print(f"\n✅ CONVERSIÓN COMPLETADA")
    print(f"📊 Total de cambios realizados: {total_changes}")
    print(f"📁 Respaldos creados en archivos .backup_*")
    
    if total_changes > 0:
        print(f"\n🎯 PRÓXIMOS PASOS:")
        print(f"1. Ejecutar regeneración de base de datos con precios en pesos")
        print(f"2. Probar cada interfaz del sistema")
        print(f"3. Verificar impresión térmica")
        print(f"4. Validar cálculos y formatos")

if __name__ == "__main__":
    main()
