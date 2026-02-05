# Script PowerShell pour lancer et maintenir le bot 24/24

$botPath = "c:\Users\Lilia\iCloudDrive\Volley\VolleyBot"
$pythonExe = "python"  # Ou le chemin complet vers python.exe
$logPath = "$botPath\bot_logs.txt"

# Créer le dossier logs s'il n'existe pas
if (!(Test-Path $botPath)) {
    Write-Host "❌ Le chemin du bot n'existe pas: $botPath"
    exit 1
}

# Boucle infinie pour relancer le bot
while ($true) {
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    
    Write-Host "[$timestamp] 🚀 Démarrage du bot VolleyBot..."
    Add-Content -Path $logPath -Value "[$timestamp] Démarrage du bot"
    
    # Lancer le bot
    & $pythonExe "$botPath\main.py"
    
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    Write-Host "[$timestamp] ⚠️ Le bot s'est arrêté. Redémarrage dans 10 secondes..."
    Add-Content -Path $logPath -Value "[$timestamp] Bot arrêté. Redémarrage..."
    
    # Attendre 10 secondes avant de redémarrer
    Start-Sleep -Seconds 10
}
