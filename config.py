"""
Configuration du bot Discord VolleyBot
"""
import os
from dotenv import load_dotenv

load_dotenv()

# Token Discord du bot (à configurer via variables d'environnement)
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
if not DISCORD_TOKEN:
    raise ValueError("❌ DISCORD_TOKEN n'est pas défini! Ajoutez-le à votre .env ou aux variables d'environnement.")

# Clé API Volleyball (à configurer via variables d'environnement)
VOLLEYBALL_API_KEY = os.getenv('VOLLEYBALL_API_KEY')
if not VOLLEYBALL_API_KEY:
    raise ValueError("❌ VOLLEYBALL_API_KEY n'est pas défini! Ajoutez-le à votre .env ou aux variables d'environnement.")

VOLLEYBALL_API_BASE_URL = "https://v1.volleyball.api-sports.io"

# Configuration du bot
BOT_PREFIX = "/"
BOT_NAME = "VolleyBot"
