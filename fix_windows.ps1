# PowerShell Script para solucionar problemas de POS en Windows 11
# Ejecutar como administrador: Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

Write-Host "🔧 Script de Reparación - POS Windows 11" -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan

# Verificar si se ejecuta como administrador
$currentPrincipal = New-Object Security.Principal.WindowsPrincipal([Security.Principal.WindowsIdentity]::GetCurrent())
$isAdmin = $currentPrincipal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)

if (-not $isAdmin) {
    Write-Host "⚠️  Recomendado ejecutar como administrador para mejores resultados" -ForegroundColor Yellow
}

# Verificar Python
Write-Host "`n1. Verificando Python..." -ForegroundColor Blue
try {
    $pythonVersion = python --version 2>&1
    Write-Host "   ✅ $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "   ❌ Python no encontrado. Instalar Python 3.7+ desde python.org" -ForegroundColor Red
    exit 1
}

# Verificar pip
Write-Host "`n2. Verificando pip..." -ForegroundColor Blue
try {
    $pipVersion = pip --version 2>&1
    Write-Host "   ✅ pip disponible" -ForegroundColor Green
} catch {
    Write-Host "   ❌ pip no encontrado" -ForegroundColor Red
    exit 1
}

# Configurar variables de entorno
Write-Host "`n3. Configurando variables de entorno..." -ForegroundColor Blue
[Environment]::SetEnvironmentVariable("QT_QPA_PLATFORM", "windows", "User")
[Environment]::SetEnvironmentVariable("QT_AUTO_SCREEN_SCALE_FACTOR", "1", "User")
$env:QT_QPA_PLATFORM = "windows"
$env:QT_AUTO_SCREEN_SCALE_FACTOR = "1"
Write-Host "   ✅ Variables Qt configuradas" -ForegroundColor Green

# Actualizar pip
Write-Host "`n4. Actualizando pip..." -ForegroundColor Blue
pip install --upgrade pip

# Desinstalar y reinstalar PyQt5
Write-Host "`n5. Reinstalando PyQt5..." -ForegroundColor Blue
pip uninstall PyQt5 -y
pip install PyQt5==5.15.9

# Instalar dependencias
Write-Host "`n6. Instalando dependencias..." -ForegroundColor Blue
if (Test-Path "requirements.txt") {
    pip install -r requirements.txt --force-reinstall
    Write-Host "   ✅ Dependencias instaladas desde requirements.txt" -ForegroundColor Green
} else {
    Write-Host "   ⚠️  requirements.txt no encontrado, instalando dependencias básicas..." -ForegroundColor Yellow
    pip install PyQt5==5.15.9 SQLAlchemy==1.4.46 pandas numpy matplotlib openpyxl python-dateutil
}

# Verificar Visual C++ Redistributable
Write-Host "`n7. Verificando Visual C++ Redistributable..." -ForegroundColor Blue
$vcredist = Get-ItemProperty HKLM:\Software\Microsoft\Windows\CurrentVersion\Uninstall\* | 
            Where-Object { $_.DisplayName -like "*Visual C++*" -and $_.DisplayName -like "*2015-2019*" }

if ($vcredist) {
    Write-Host "   ✅ Visual C++ Redistributable 2015-2019 instalado" -ForegroundColor Green
} else {
    Write-Host "   ⚠️  Visual C++ Redistributable 2015-2019 no encontrado" -ForegroundColor Yellow
    Write-Host "   📥 Descargando..." -ForegroundColor Blue
    
    $url = "https://aka.ms/vs/17/release/vc_redist.x64.exe"
    $output = "$env:TEMP\vc_redist.x64.exe"
    
    try {
        Invoke-WebRequest -Uri $url -OutFile $output
        Write-Host "   ✅ Descarga completada. Ejecutando instalador..." -ForegroundColor Green
        Start-Process -FilePath $output -ArgumentList "/passive" -Wait
        Write-Host "   ✅ Visual C++ Redistributable instalado" -ForegroundColor Green
    } catch {
        Write-Host "   ❌ Error al descargar/instalar VC++ Redistributable" -ForegroundColor Red
        Write-Host "   💡 Descargar manualmente desde: $url" -ForegroundColor Yellow
    }
}

# Test de PyQt5
Write-Host "`n8. Probando PyQt5..." -ForegroundColor Blue
$testResult = python -c "
try:
    from PyQt5.QtWidgets import QApplication
    import sys
    app = QApplication([])
    print('✅ PyQt5 OK')
    app.quit()
except Exception as e:
    print(f'❌ Error: {e}')
    exit(1)
"

if ($LASTEXITCODE -eq 0) {
    Write-Host "   ✅ PyQt5 funciona correctamente" -ForegroundColor Green
} else {
    Write-Host "   ❌ PyQt5 tiene problemas" -ForegroundColor Red
}

# Ejecutar diagnóstico
Write-Host "`n9. Ejecutando diagnóstico..." -ForegroundColor Blue
if (Test-Path "diagnose_windows.py") {
    python diagnose_windows.py
} else {
    Write-Host "   ⚠️  diagnose_windows.py no encontrado" -ForegroundColor Yellow
}

# Test mínimo
Write-Host "`n10. Ejecutando test mínimo..." -ForegroundColor Blue
if (Test-Path "test_minimal.py") {
    Write-Host "   🧪 Ejecutando test visual..." -ForegroundColor Blue
    python test_minimal.py
} else {
    Write-Host "   ⚠️  test_minimal.py no encontrado" -ForegroundColor Yellow
}

# Configurar Windows Defender
Write-Host "`n11. Configurando exclusiones de Windows Defender..." -ForegroundColor Blue
if ($isAdmin) {
    try {
        $projectPath = Get-Location
        Add-MpPreference -ExclusionPath $projectPath.Path
        
        # Encontrar python.exe
        $pythonPath = (Get-Command python).Source
        Add-MpPreference -ExclusionProcess $pythonPath
        
        Write-Host "   ✅ Exclusiones de Windows Defender añadidas" -ForegroundColor Green
    } catch {
        Write-Host "   ⚠️  No se pudieron añadir exclusiones de Windows Defender" -ForegroundColor Yellow
    }
} else {
    Write-Host "   ⚠️  Se requieren permisos de administrador para configurar Windows Defender" -ForegroundColor Yellow
}

# Intentar ejecutar la aplicación
Write-Host "`n12. Intentando ejecutar la aplicación..." -ForegroundColor Blue
Write-Host "=====================================" -ForegroundColor Cyan

if (Test-Path "main.py") {
    Write-Host "🚀 Ejecutando Sistema POS..." -ForegroundColor Green
    python main.py
} elseif (Test-Path "main_debug.py") {
    Write-Host "🚀 Ejecutando Sistema POS en modo debug..." -ForegroundColor Green
    python main_debug.py --debug
} else {
    Write-Host "❌ main.py no encontrado en el directorio actual" -ForegroundColor Red
    Write-Host "   📁 Verificar que estás en el directorio correcto del proyecto" -ForegroundColor Yellow
}

Write-Host "`n✅ Script de reparación completado" -ForegroundColor Green
Write-Host "📋 Si persisten problemas:" -ForegroundColor Yellow
Write-Host "   1. Reiniciar el sistema" -ForegroundColor White
Write-Host "   2. Verificar que no hay otro software usando PyQt5" -ForegroundColor White
Write-Host "   3. Probar con un entorno virtual limpio" -ForegroundColor White
Write-Host "   4. Contactar soporte técnico con los logs generados" -ForegroundColor White

Read-Host "`nPresiona Enter para salir"
