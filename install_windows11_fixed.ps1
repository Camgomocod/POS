# Instalador de Dependencias y Accesos Directos para Windows 11
# POS RestauranteFast

param(
    [switch]$Force,
    [switch]$InstallDeps,
    [switch]$CreateShortcuts,
    [switch]$All
)

# Configurar encoding para consola
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

# Colores para output
$Host.UI.RawUI.WindowTitle = "POS RestauranteFast - Instalador Windows 11"

function Write-ColorOutput {
    param(
        [string]$Message,
        [string]$Color = "White"
    )
    Write-Host $Message -ForegroundColor $Color
}

function Test-PythonInstallation {
    Write-ColorOutput "Verificando instalacion de Python..." "Cyan"
    
    $pythonCommands = @("py", "python", "python3")
    $pythonFound = $false
    
    foreach ($cmd in $pythonCommands) {
        try {
            $version = & $cmd --version 2>$null
            if ($LASTEXITCODE -eq 0) {
                Write-ColorOutput "OK - $cmd encontrado: $version" "Green"
                $pythonFound = $true
                break
            }
        }
        catch {
            # Continuar con el siguiente comando
        }
    }
    
    if (-not $pythonFound) {
        Write-ColorOutput "ERROR - Python no encontrado" "Red"
        Write-ColorOutput "Descarga Python desde: https://python.org" "Yellow"
        Write-ColorOutput "IMPORTANTE: Marca 'Add to PATH' durante la instalacion" "Yellow"
        return $false
    }
    
    return $true
}

function Install-PythonDependencies {
    Write-ColorOutput "Instalando dependencias de Python..." "Cyan"
    
    # Intentar pip install
    $pipCommands = @("pip", "pip3", "py -m pip", "python -m pip")
    $pipSuccess = $false
    
    foreach ($pipCmd in $pipCommands) {
        try {
            Write-ColorOutput "Probando: $pipCmd" "Gray"
            Invoke-Expression "$pipCmd install --upgrade pip" 2>$null
            if ($LASTEXITCODE -eq 0) {
                # Instalar dependencias principales
                $packages = @(
                    "PyQt5",
                    "SQLAlchemy", 
                    "Faker",
                    "winshell",
                    "pywin32"
                )
                
                foreach ($package in $packages) {
                    Write-ColorOutput "Instalando $package..." "Yellow"
                    Invoke-Expression "$pipCmd install $package"
                    if ($LASTEXITCODE -eq 0) {
                        Write-ColorOutput "OK - $package instalado" "Green"
                    } else {
                        Write-ColorOutput "ERROR instalando $package" "Red"
                    }
                }
                
                $pipSuccess = $true
                break
            }
        }
        catch {
            continue
        }
    }
    
    return $pipSuccess
}

function Create-DesktopShortcut {
    Write-ColorOutput "Creando acceso directo en escritorio..." "Cyan"
    
    try {
        $WshShell = New-Object -ComObject WScript.Shell
        $DesktopPath = [System.Environment]::GetFolderPath("Desktop")
        $ShortcutPath = Join-Path $DesktopPath "POS RestauranteFast.lnk"
        $Shortcut = $WshShell.CreateShortcut($ShortcutPath)
        
        $CurrentPath = Get-Location
        $BatchFile = Join-Path $CurrentPath "POS_Windows11.bat"
        
        $Shortcut.TargetPath = $BatchFile
        $Shortcut.WorkingDirectory = $CurrentPath
        $Shortcut.Description = "Sistema POS para Restaurantes"
        $Shortcut.IconLocation = Join-Path $CurrentPath "assets\pos_icon.ico"
        $Shortcut.Save()
        
        Write-ColorOutput "OK - Acceso directo creado: $ShortcutPath" "Green"
        return $true
    }
    catch {
        Write-ColorOutput "ERROR creando acceso directo: $_" "Red"
        return $false
    }
}

function Create-StartMenuEntry {
    Write-ColorOutput "Agregando al menu inicio..." "Cyan"
    
    try {
        $StartMenuPath = Join-Path $env:APPDATA "Microsoft\Windows\Start Menu\Programs"
        $ShortcutPath = Join-Path $StartMenuPath "POS RestauranteFast.lnk"
        
        $WshShell = New-Object -ComObject WScript.Shell
        $Shortcut = $WshShell.CreateShortcut($ShortcutPath)
        
        $CurrentPath = Get-Location
        $BatchFile = Join-Path $CurrentPath "POS_Windows11.bat"
        
        $Shortcut.TargetPath = $BatchFile
        $Shortcut.WorkingDirectory = $CurrentPath
        $Shortcut.Description = "Sistema POS para Restaurantes"
        $Shortcut.IconLocation = Join-Path $CurrentPath "assets\pos_icon.ico"
        $Shortcut.Save()
        
        Write-ColorOutput "OK - Entrada agregada al menu inicio" "Green"
        return $true
    }
    catch {
        Write-ColorOutput "ERROR agregando al menu inicio: $_" "Red"
        return $false
    }
}

function Show-Instructions {
    Write-ColorOutput "" "White"
    Write-ColorOutput "================================================================" "Cyan"
    Write-ColorOutput "                    INSTALACION COMPLETADA                       " "Green"
    Write-ColorOutput "================================================================" "Cyan"
    Write-ColorOutput "" "White"
    Write-ColorOutput "FORMAS DE EJECUTAR LA APLICACION:" "White"
    Write-ColorOutput "----------------------------------------------------------------" "Gray"
    Write-ColorOutput "1. Doble click en 'POS RestauranteFast' (escritorio)" "Yellow"
    Write-ColorOutput "2. Buscar 'POS RestauranteFast' en menu inicio" "Yellow"
    Write-ColorOutput "3. Ejecutar 'POS_Windows11.bat' en esta carpeta" "Yellow"
    Write-ColorOutput "" "White"
    Write-ColorOutput "CREDENCIALES DE ACCESO:" "White"
    Write-ColorOutput "----------------------------------------------------------------" "Gray"
    Write-ColorOutput "Administrador: admin / admin123" "Green"
    Write-ColorOutput "Cajero: cajero / cajero123" "Green"
    Write-ColorOutput "" "White"
    Write-ColorOutput "TESTING RECOMENDADO:" "White"
    Write-ColorOutput "----------------------------------------------------------------" "Gray"
    Write-ColorOutput "- Dia 1-2: Configurar productos y categorias" "Cyan"
    Write-ColorOutput "- Dia 3-4: Procesar ventas y pagos" "Cyan"
    Write-ColorOutput "- Dia 5-7: Generar reportes y analisis" "Cyan"
    Write-ColorOutput "" "White"
    Write-ColorOutput "Archivos importantes:" "White"
    Write-ColorOutput "----------------------------------------------------------------" "Gray"
    Write-ColorOutput "- README_WINDOWS11.md - Guia completa de uso" "Yellow"
    Write-ColorOutput "- data\pos.db - Base de datos (hacer backup)" "Yellow"
    Write-ColorOutput "================================================================" "Cyan"
}

# Script principal
Clear-Host
Write-ColorOutput "================================================================" "Cyan"
Write-ColorOutput "           POS RestauranteFast - Instalador Windows 11          " "Cyan"
Write-ColorOutput "                   Sistema de Punto de Venta                   " "Cyan"
Write-ColorOutput "================================================================" "Cyan"

# Verificar ubicación
if (-not (Test-Path "main.py")) {
    Write-ColorOutput "" "White"
    Write-ColorOutput "ERROR: Este script debe ejecutarse desde la carpeta del proyecto POS" "Red"
    Write-ColorOutput "Directorio actual: $(Get-Location)" "Yellow"
    Write-ColorOutput "Navega a la carpeta que contiene main.py y ejecuta nuevamente" "Yellow"
    Read-Host "`nPresiona Enter para salir"
    exit 1
}

# Determinar qué hacer
if ($All) {
    $InstallDeps = $true
    $CreateShortcuts = $true
}

if (-not $InstallDeps -and -not $CreateShortcuts) {
    Write-ColorOutput "" "White"
    Write-ColorOutput "Que deseas hacer?" "White"
    Write-ColorOutput "1. Solo crear accesos directos" "Yellow"
    Write-ColorOutput "2. Solo instalar dependencias" "Yellow"
    Write-ColorOutput "3. Instalacion completa (recomendado)" "Green"
    
    $choice = Read-Host "`nSelecciona opcion (1-3)"
    
    switch ($choice) {
        "1" { $CreateShortcuts = $true }
        "2" { $InstallDeps = $true }
        "3" { 
            $InstallDeps = $true
            $CreateShortcuts = $true
        }
        default {
            Write-ColorOutput "Opcion invalida. Ejecutando instalacion completa." "Red"
            $InstallDeps = $true
            $CreateShortcuts = $true
        }
    }
}

$success = $true

# Verificar Python
if (-not (Test-PythonInstallation)) {
    $success = $false
    Write-ColorOutput "`nInstala Python antes de continuar" "Red"
} else {
    # Instalar dependencias si se solicitó
    if ($InstallDeps) {
        if (-not (Install-PythonDependencies)) {
            Write-ColorOutput "Algunas dependencias pueden no haberse instalado correctamente" "Yellow"
        }
    }
    
    # Crear accesos directos si se solicitó
    if ($CreateShortcuts) {
        # Crear directorio assets si no existe
        $assetsDir = "assets"
        if (-not (Test-Path $assetsDir)) {
            New-Item -ItemType Directory -Path $assetsDir -Force | Out-Null
        }
        
        # Crear archivo de icono básico
        $iconPath = Join-Path $assetsDir "pos_icon.ico"
        if (-not (Test-Path $iconPath)) {
            "# POS Icon Placeholder" | Out-File -FilePath $iconPath -Encoding UTF8
        }
        
        Create-DesktopShortcut | Out-Null
        Create-StartMenuEntry | Out-Null
    }
}

if ($success) {
    Show-Instructions
} else {
    Write-ColorOutput "`nInstalacion incompleta. Revisa los errores anteriores." "Red"
}

Write-ColorOutput "`nPresiona Enter para finalizar..." "Gray"
Read-Host
