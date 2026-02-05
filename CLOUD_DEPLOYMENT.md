# 🌐 Héberger VolleyBot sur le Cloud 24/24

**Votre PC peut être ÉTEINT et le bot fonctionne toujours!**

---

## ✅ Solution 1: Railway (MEILLEURE - 5 minutes)

### Étape 1: Créer un compte GitHub
1. Allez sur https://github.com
2. Créez un compte (gratuit)
3. Confirmez votre email

### Étape 2: Créer un repo pour votre bot
1. Cliquez sur le "+" en haut à droite → "New repository"
2. Nom: `VolleyBot`
3. Description: "Bot Discord pour le volley"
4. Sélectionnez "Public" (ou Private)
5. Cliquez "Create repository"

### Étape 3: Uploader votre code
Option A - Avec Git (recommandé):

```powershell
cd "c:\Users\Lilia\iCloudDrive\Volley\VolleyBot"

# Initialiser git
git init
git add .
git commit -m "Initial commit - VolleyBot"
git branch -M main
git remote add origin https://github.com/VOTRE_USERNAME/VolleyBot.git
git push -u origin main
```

Option B - Via l'interface GitHub:
1. Cliquez sur "uploading an existing file"
2. Déposez vos fichiers (ctrl+clic sur le dossier)

### Étape 4: Configurer Railway
1. Allez sur https://railway.app
2. Cliquez "Start a New Project"
3. Choisissez "Deploy from GitHub repo"
4. Connectez votre compte GitHub
5. Sélectionnez votre repo `VolleyBot`
6. Railway va analyser et déployer automatiquement!

### Étape 5: Ajouter les variables d'environnement
1. Dans Railway, allez à l'onglet "Variables"
2. Cliquez "Add Variable"
3. Ajoutez:
   - **Clé**: `DISCORD_TOKEN`
   - **Valeur**: `XXXXXXXXXXXXXXXXXXXXXXXXXXXSS`

4. Cliquez "Add Variable" à nouveau
   - **Clé**: `VOLLEYBALL_API_KEY`
   - **Valeur**: `XXXXXXXXXXXXXXXXXXXXXXXXX`

5. Cliquez "Deploy"

### ✅ Voilà! Votre bot est en ligne! 🎉

---

## 📊 Comparaison des solutions cloud

| Platform | Coût | Facilité | Fiabilité | Gratuit |
|----------|------|---------|-----------|---------|
| **Railway** | $5/mois | ⭐⭐⭐ | ⭐⭐⭐⭐ | ✅ $5 gratuit |
| **Replit** | Gratuit | ⭐⭐⭐ | ⭐⭐⭐ | ✅ Oui |
| **Render** | Gratuit | ⭐⭐⭐ | ⭐⭐⭐ | ✅ Oui (pause après 15min inactivité) |
| **Oracle Cloud** | Gratuit | ⭐⭐ | ⭐⭐⭐⭐ | ✅ Oui (compliqué) |
| **VPS OVH** | 2€/mois | ⭐⭐ | ⭐⭐⭐⭐ | ❌ Payant |

---

## 🚀 Solution 2: Replit (Gratuit, plus facile)

1. Allez sur https://replit.com
2. Cliquez "Create"
3. Choisissez "Import from GitHub"
4. Collez: `https://github.com/VOTRE_USERNAME/VolleyBot`
5. Cliquez "Import"
6. Installez les dépendances:
   ```bash
   pip install -r requirements.txt
   ```
7. Cliquez "Run" et c'est parti!

**Important**: Sur Replit gratuit, le bot s'arrête après 1h d'inactivité. Utilisez un service comme:
- https://uptimerobot.com (gratuit)
- https://www.statuscake.com (gratuit)

---

## 🔧 Solution 3: VPS OVH (Meilleur prix - 2€/mois)

### Avantages:
- Très bon marché (2€/mois)
- Fonctionne 24/24 sans interruption
- Performant
- Vous contrôlez tout

### Installation rapide:

1. Créez un compte OVH: https://www.ovh.com/fr/
2. Achetez un VPS "VPS Cloud" (2€/mois)
3. Récupérez l'IP et le mot de passe
4. Ouvrez PowerShell et connectez-vous:
```powershell
# Sur Windows: installez PuTTY ou utilisez SSH
ssh root@your_server_ip
```

5. Copié-collé ces commandes:
```bash
# Mettre à jour le système
apt update && apt upgrade -y

# Installer Python et Git
apt install -y python3 python3-pip git

# Cloner votre repo
git clone https://github.com/VOTRE_USERNAME/VolleyBot.git
cd VolleyBot

# Installer les dépendances
pip install -r requirements.txt

# Lancer le bot en arrière-plan (détaché)
nohup python3 main.py > bot.log 2>&1 &

# Vérifier que ça marche
ps aux | grep main.py
```

6. **C'est prêt!** Le bot fonctionne 24/24 sur votre serveur 🚀

### Voir les logs:
```bash
tail -f bot.log
```

### Arrêter le bot:
```bash
pkill -f main.py
```

---

## 📲 Monitorer votre bot (Gratuit)

### Uptime Robot (Surveille si votre bot est en ligne)

1. Allez sur https://uptimerobot.com
2. Créez un compte
3. Ajoutez un monitor: Ping Check
4. URL: `https://discord.com/api/v10/applications/@me` (avec votre token)
5. Vous recevez des alertes par email si ça plante

---

## 🆘 Troubleshooting

### "Le bot ne démarre pas sur Railway"

Vérifiez:
1. Les variables d'environnement sont bien configurées
2. Les fichiers `Procfile`, `Dockerfile`, `requirements.txt` existent
3. Regardez les logs Railway (onglet "Logs")

### "Le token est invalide"

- Régénérez-le sur https://discord.com/developers/applications
- Vérifiez que vous avez copié le bon token (pas d'espaces)

### "ImportError: No module named discord"

Vérifiez que `discord.py` est dans `requirements.txt`

---

## ✅ Résumé - Étapes finales

**Si vous avez fait les étapes ci-dessus:**

1. ✅ Repo GitHub créé
2. ✅ Code uploadé
3. ✅ Railway configuré avec variables
4. ✅ Bot lancé

**Bravo! Votre bot fonctionne 24/24! 🎉**

Pour tester:
```
/volleybot classement Paris
```

Si ça marche, c'est bon! Sinon, vérifiez les logs.

---

## 💡 Bonus: Mettre à jour le bot

Après chaque modification:

```powershell
cd "c:\Users\Lilia\iCloudDrive\Volley\VolleyBot"
git add .
git commit -m "Mise à jour - description"
git push origin main
```

Railway redéploiera automatiquement! 🚀
