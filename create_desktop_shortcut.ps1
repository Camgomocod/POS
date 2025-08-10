# Script PowerShell para crear acceso directo del Sistema POS
# create_desktop_shortcut.ps1

param(
    [string]$ProjectPath = (Get-Location).Path,
    [string]$ShortcutName = "Sistema POS"
)

Write-Host "╔══════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║           CREADOR DE ACCESO DIRECTO - SISTEMA POS        ║" -ForegroundColor Cyan  
Write-Host "╚══════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# Verificar que estamos en la carpeta correcta
if (-not (Test-Path "$ProjectPath\main.py")) {
    Write-Host "❌ Error: No se encuentra main.py en $ProjectPath" -ForegroundColor Red
    Write-Host "💡 Asegúrate de ejecutar este script desde la carpeta del proyecto POS" -ForegroundColor Yellow
    Read-Host "Presiona Enter para salir"
    exit 1
}

Write-Host "📁 Carpeta del proyecto: $ProjectPath" -ForegroundColor Green

# Obtener ruta del escritorio
$DesktopPath = [Environment]::GetFolderPath("Desktop")
Write-Host "🖥️  Escritorio: $DesktopPath" -ForegroundColor Green

# Crear acceso directo principal
$ShortcutPath = "$DesktopPath\$ShortcutName.lnk"

try {
    $WshShell = New-Object -ComObject WScript.Shell
    $Shortcut = $WshShell.CreateShortcut($ShortcutPath)
    
    # Configurar acceso directo para run_pos.bat
    $Shortcut.TargetPath = "cmd.exe"
    $Shortcut.Arguments = "/k `"cd /d `"$ProjectPath`" && run_pos.bat`""
    $Shortcut.WorkingDirectory = $ProjectPath
    $Shortcut.IconLocation = "shell32.dll,137"  # Icono de monitor
    $Shortcut.Description = "Sistema POS - Restaurante Fast Food"
    $Shortcut.WindowStyle = 1  # Ventana normal
    
    $Shortcut.Save()
    Write-Host "✅ Acceso directo principal creado: $ShortcutName.lnk" -ForegroundColor Green
    
} catch {
    Write-Host "❌ Error al crear acceso directo principal: $($_.Exception.Message)" -ForegroundColor Red
}

# Crear acceso directo de instalación
$InstallShortcutPath = "$DesktopPath\Instalar $ShortcutName.lnk"

try {
    $InstallShortcut = $WshShell.CreateShortcut($InstallShortcutPath)
    
    $InstallShortcut.TargetPath = "cmd.exe"
    $InstallShortcut.Arguments = "/k `"cd /d `"$ProjectPath`" && install_pos_w11.bat`""
    $InstallShortcut.WorkingDirectory = $ProjectPath
    $InstallShortcut.IconLocation = "shell32.dll,21"  # Icono de instalación
    $InstallShortcut.Description = "Instalar Sistema POS - Configuración inicial"
    $InstallShortcut.WindowStyle = 1
    
    $InstallShortcut.Save()
    Write-Host "✅ Acceso directo de instalación creado: Instalar $ShortcutName.lnk" -ForegroundColor Green
    
} catch {
    Write-Host "❌ Error al crear acceso directo de instalación: $($_.Exception.Message)" -ForegroundColor Red
}

# Crear acceso directo de inicio rápido
$QuickStartPath = "$DesktopPath\$ShortcutName - Inicio Rápido.lnk"

try {
    $QuickShortcut = $WshShell.CreateShortcut($QuickStartPath)
    
    $QuickShortcut.TargetPath = "cmd.exe"
    $QuickShortcut.Arguments = "/k `"cd /d `"$ProjectPath`" && quick_start.bat`""
    $QuickShortcut.WorkingDirectory = $ProjectPath
    $QuickShortcut.IconLocation = "shell32.dll,25"  # Icono de velocidad
    $QuickShortcut.Description = "Sistema POS - Inicio Rápido (sin verificaciones)"
    $QuickShortcut.WindowStyle = 1
    
    $QuickShortcut.Save()
    Write-Host "✅ Acceso directo de inicio rápido creado: $ShortcutName - Inicio Rápido.lnk" -ForegroundColor Green
    
} catch {
    Write-Host "❌ Error al crear acceso directo de inicio rápido: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host ""
Write-Host "╔══════════════════════════════════════════════════════════╗" -ForegroundColor Green
Write-Host "║                 ✅ ACCESOS DIRECTOS CREADOS               ║" -ForegroundColor Green
Write-Host "╚══════════════════════════════════════════════════════════╝" -ForegroundColor Green
Write-Host ""

Write-Host "🖥️  Accesos directos creados en el escritorio:" -ForegroundColor Cyan
Write-Host ""
Write-Host "   1. 📊 $ShortcutName.lnk" -ForegroundColor White
Write-Host "      → Ejecuta el sistema con todas las verificaciones" -ForegroundColor Gray
Write-Host ""
Write-Host "   2. 🔧 Instalar $ShortcutName.lnk" -ForegroundColor White  
Write-Host "      → Instala dependencias y configura el entorno" -ForegroundColor Gray
Write-Host ""
Write-Host "   3. ⚡ $ShortcutName - Inicio Rápido.lnk" -ForegroundColor White
Write-Host "      → Inicia directamente sin verificaciones (más rápido)" -ForegroundColor Gray
Write-Host ""

Write-Host "💡 Uso recomendado:" -ForegroundColor Yellow
Write-Host "   • Primera vez: Usar 'Instalar Sistema POS'" -ForegroundColor Yellow
Write-Host "   • Uso normal: Usar 'Sistema POS'" -ForegroundColor Yellow  
Write-Host "   • Uso experto: Usar 'Sistema POS - Inicio Rápido'" -ForegroundColor Yellow
Write-Host ""

Write-Host "👤 Credenciales por defecto:" -ForegroundColor Magenta
Write-Host "   Admin: admin / admin123" -ForegroundColor White
Write-Host "   Cajero: cajero / cajero123" -ForegroundColor White
Write-Host ""

Read-Host "Presiona Enter para finalizar"
