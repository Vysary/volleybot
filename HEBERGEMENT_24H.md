# Guide d'hébergement 24/24 pour VolleyBot 🏐

## Option 1: Windows Task Scheduler (⭐ Recommandé)

### Avantages:
✅ Gratuit et intégré à Windows  
✅ Relance automatique si le bot crash  
✅ Dépend de votre PC (gratuit)  
✅ Configuration facile  

### Inconvénients:
❌ Votre PC doit rester allumé 24/24  
❌ Consomme des ressources  

### Installation (Méthode 1: Automatique)

**Étape 1:** Ouvrez PowerShell en tant qu'administrateur
```powershell
# Clic droit sur le menu Démarrer > PowerShell (Admin)
```

**Étape 2:** Exécutez le script d'installation
```powershell
Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process
cd "c:\Users\Lilia\iCloudDrive\Volley\VolleyBot"
.\install_scheduler.ps1
```

**Étape 3:** C'est fait ! 🎉 Le bot démarre maintenant automatiquement.

### Installation (Méthode 2: Manuelle)

Si vous préférez configurer manuellement:

1. Appuyez sur `Win + R` et tapez: `taskschd.msc`
2. Clic droit → "Créer une tâche basique"
3. Nom: `VolleyBot`
4. Onglet "Déclencheurs":
   - Nouveau → "À la connexion"
   - Utilisateur: `Lilia`
5. Onglet "Actions":
   - Action: "Démarrer un programme"
   - Programme: `c:\Users\Lilia\iCloudDrive\Volley\VolleyBot\run_bot.bat`
6. Onglet "Paramètres":
   - ✅ "Laisser la tâche s'exécuter aussi longtemps que nécessaire"
   - ✅ "Si la tâche échoue, redémarrer"
7. OK

---

## Option 2: Service Windows (⭐⭐ Plus avancé)

### Avantages:
✅ Le bot s'exécute même quand vous êtes déconnecté  
✅ Fonctionnement 100% transparent  
✅ Plus professionnel  

### Installation:

1. Installez NSSM (Non-Sucking Service Manager) - gratuit et simple:
```powershell
# Téléchargez depuis: https://nssm.cc/download
# Décompressez dans: c:\nssm\
```

2. Ouvrez PowerShell en tant qu'administrateur:
```powershell
cd "c:\nssm\win64"
.\nssm.exe install VolleyBot "C:\Program Files\Python311\python.exe" "c:\Users\Lilia\iCloudDrive\Volley\VolleyBot\main.py"
.\nssm.exe start VolleyBot
```

3. Pour arrêter le service:
```powershell
.\nssm.exe stop VolleyBot
```

---

## Option 3: Hébergement Cloud Gratuit ⭐⭐⭐ (Recommandé si PC limité)

### Replit (Facile, gratuit avec limitations)

**Pros:**
✅ Pas besoin de votre PC  
✅ Gratuit  
✅ Configuration facile  

**Cons:**
❌ Limité en puissance (gratuit)  
❌ Peut s'arrêter si inactif longtemps  

**Démarche:**
1. Allez sur https://replit.com
2. Créez un compte
3. Créez un nouveau projet "Python"
4. Uploadez vos fichiers
5. Installez les dépendances: `pip install -r requirements.txt`
6. Cliquez sur "Run"
7. Utilisez Uptimerobot (gratuit) pour garder alive

### Railway (Très simple)

**Pros:**
✅ Gratuit pour les premiers $5/mois  
✅ Très facile  
✅ Fiable  

**Démarche:**
1. Allez sur https://railway.app
2. Se connecter avec GitHub
3. Créer un nouveau projet
4. Connecter votre repo GitHub
5. Ajouter variable `DISCORD_TOKEN`
6. Déployer

### Heroku (Payant mais performant)

https://www.heroku.com - Environ $5/mois

---

## Option 4: VPS (Meilleure performance - Payant)

Services recommandés:
- **OVH** - à partir de 2€/mois
- **Linode** - à partir de $5/mois (gratuit 60€ crédit)
- **DigitalOcean** - à partir de $4/mois
- **Scaleway** - à partir de €3/mois

Installation simple:
```bash
ssh root@your_server_ip
apt update && apt install python3 python3-pip
git clone <votre_repo>
cd VolleyBot
pip install -r requirements.txt
nohup python main.py &
```

---

## Monitoring & Logs

### Voir les logs du bot

**Avec Task Scheduler:**
```powershell
# Afficher les logs
Get-Content "c:\Users\Lilia\iCloudDrive\Volley\VolleyBot\bot_logs.txt" -Tail 50

# Afficher en temps réel
Get-Content "c:\Users\Lilia\iCloudDrive\Volley\VolleyBot\bot_logs.txt" -Tail 50 -Wait
```

### Vérifier l'état du bot

```powershell
Get-ScheduledTask -TaskName VolleyBot | Select-Object TaskName, State
```

### Forcer un redémarrage

```powershell
Stop-ScheduledTask -TaskName VolleyBot
Start-ScheduledTask -TaskName VolleyBot
```

---

## Conseils d'optimisation

### 1. Ajouter des logs détaillés
Modifiez `main.py` pour enregistrer les erreurs:

```python
import logging

logging.basicConfig(
    filename='bot_logs.txt',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
```

### 2. Monitorer la santé du bot

Installez un service de monitoring gratuit:
```
- Uptime Robot (https://uptimerobot.com)
- Healthchecks.io (https://healthchecks.io)
```

### 3. Auto-redémarrage quotidien

Ajouter un redémarrage chaque jour à 3h du matin:
```powershell
$trigger = @(
    New-ScheduledTaskTrigger -AtLogOn
    New-ScheduledTaskTrigger -Daily -At 03:00
)
```

---

## Résumé rapide

| Méthode | Coût | Facilité | Fiabilité | PC allumé |
|---------|------|---------|-----------|-----------|
| Task Scheduler | Gratuit | ⭐⭐⭐ | ⭐⭐ | ✅ Oui |
| Service Windows | Gratuit | ⭐⭐ | ⭐⭐⭐ | ✅ Oui |
| Replit | Gratuit | ⭐⭐⭐ | ⭐⭐ | ❌ Non |
| Railway | Gratuit/5$ | ⭐⭐⭐ | ⭐⭐⭐ | ❌ Non |
| VPS | 2-10€/mois | ⭐⭐ | ⭐⭐⭐⭐ | ❌ Non |

**Mon recommandation:** 
- Débutant avec PC allumé → **Task Scheduler**
- PC s'éteint souvent → **Railway** (gratuit)
- Besoin de performance → **VPS OVH** (2€/mois)
