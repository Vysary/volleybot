# Script d'installation du bot en tant que tâche Windows planifiée
# À exécuter en tant qu'administrateur

# Configuration
$taskName = "VolleyBot"
$scriptPath = "c:\Users\Lilia\iCloudDrive\Volley\VolleyBot\run_bot.bat"
$username = $env:USERNAME

# Vérifier si la tâche existe déjà
$existingTask = Get-ScheduledTask -TaskName $taskName -ErrorAction SilentlyContinue

if ($existingTask) {
    Write-Host "❌ La tâche '$taskName' existe déjà. Suppression..."
    Unregister-ScheduledTask -TaskName $taskName -Confirm:$false
}

Write-Host "✅ Installation de la tâche planifiée '$taskName'..."

# Créer les arguments pour PowerShell
$action = New-ScheduledTaskAction -Execute "powershell.exe" -Argument "-NoProfile -ExecutionPolicy Bypass -File $scriptPath"

# Lancer à la connexion (trigger)
$trigger = New-ScheduledTaskTrigger -AtLogOn -User $username

# Options de la tâche
$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable

# Enregistrer la tâche
Register-ScheduledTask -Action $action -Trigger $trigger -Settings $settings -TaskName $taskName -Description "Bot Discord VolleyBot - Fonctionne 24/7"

Write-Host "✅ Tâche '$taskName' créée avec succès!"
Write-Host "📌 Le bot démarrera automatiquement à chaque connexion"
Write-Host "📌 Le bot se relancera automatiquement s'il s'arrête"

# Afficher les détails
Write-Host "`n📊 Détails de la tâche:"
Get-ScheduledTask -TaskName $taskName | Format-List
