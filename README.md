# VolleyBot 🏐

Bot Discord pour consulter les informations sur le volley-ball en utilisant l'API Volleyball Sports.

## Fonctionnalités

- 📊 **Classement**: Affiche le classement d'une équipe
- 📅 **Matchs**: Affiche les matchs du jour selon le pays
- ⚽ **Scores**: Affiche les scores récents d'une équipe

## Installation

### Prérequis
- Python 3.8 ou supérieur
- Un token Discord (bot)
- Une clé API Volleyball Sports (https://www.api-sports.io/documentation/volleyball)

### Étapes

1. **Cloner ou créer le projet**
```bash
cd VolleyBot
```

2. **Installer les dépendances**
```bash
pip install -r requirements.txt
```

3. **Configurer les tokens**

Modifiez le fichier `config.py` et remplacez:
- `DISCORD_TOKEN` par votre token Discord
- `VOLLEYBALL_API_KEY` par votre clé API Volleyball

```python
# config.py
DISCORD_TOKEN = "votre_token_discord"
VOLLEYBALL_API_KEY = "votre_clé_api"
```

4. **Démarrer le bot**
```bash
python main.py
```

## Commandes

### /volleybot classement [équipe]
Affiche le classement d'une équipe.

**Exemple:**
```
/volleybot classement Paris
```

**Résultat:**
- Position dans le classement
- Points totaux
- Nombre de matchs joués
- Victoires/Défaites
- Ratio de points

### /volleybot matchs [pays]
Affiche les matchs du jour pour un pays.

**Exemple:**
```
/volleybot matchs France
```

**Résultat:**
- Liste des matchs programmés
- Horaires
- Équipes
- Scores (si match commencé)

### /volleybot score [équipe]
Affiche les 5 derniers matchs et scores d'une équipe.

**Exemple:**
```
/volleybot score Paris
```

**Résultat:**
- Derniers matchs
- Scores finaux
- Résultat (Victoire/Défaite)
- Dates

## Structure du projet

```
VolleyBot/
├── main.py              # Fichier principal du bot
├── config.py            # Configuration (tokens, clés API)
├── requirements.txt     # Dépendances Python
├── README.md           # Ce fichier
├── utils/
│   ├── __init__.py
│   └── api.py          # Module API Volleyball
└── cogs/
    ├── __init__.py
    └── volleyball.py   # Commandes Volleyball
```

## Aide

### Je reçois une erreur "Invalid token"
- Vérifiez que votre `DISCORD_TOKEN` est correct
- Assurez-vous que le token n'a pas d'espaces
- Régénérez le token depuis le portail Discord

### Aucune équipe n'est trouvée
- Vérifiez l'orthographe du nom de l'équipe
- Certains noms peuvent être partiels (ex: "Paris" au lieu du nom complet)

### L'API retourne une erreur
- Vérifiez votre clé API Volleyball
- Assurez-vous que votre compte API a les permissions nécessaires

## Notes de sécurité ⚠️

**IMPORTANT:** N'exposez jamais vos tokens/clés API!
- Ne commitez pas le fichier `config.py` contenant les tokens
- Utilisez un fichier `.env` en production
- Régénérez vos tokens si vous les avez partagés

Pour sécuriser vos tokens:
1. Régénérez le token Discord depuis https://discord.com/developers/applications
2. Changez votre clé API Volleyball depuis votre compte

## Support

Pour toute question ou problème, consultez:
- [Documentation Discord.py](https://discordpy.readthedocs.io/)
- [API Volleyball Sports](https://www.api-sports.io/documentation/volleyball)
