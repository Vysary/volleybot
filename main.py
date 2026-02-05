"""
Bot Discord VolleyBot
Récupère les informations sur le volley-ball
"""

import discord
from discord.ext import commands
import asyncio
import os
import logging
from dotenv import load_dotenv

# Configurer le logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('VolleyBot')

# Charger les variables d'environnement
load_dotenv()

# Récupérer le token depuis les variables d'environnement ou config.py
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN') or os.getenv('DISCORD_TOKEN')


class VolleyBot(commands.Bot):
    """Classe principale du bot Discord"""
    
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.guilds = True
        
        super().__init__(
            command_prefix="/",
            intents=intents,
            help_command=None
        )
    
    async def setup_hook(self):
        """Configuration initiale du bot"""
        # Charger les cogs
        await self.load_cogs()
    
    async def load_cogs(self):
        """Charge tous les cogs du dossier cogs"""
        # Utiliser le chemin absolu basé sur le répertoire courant du script
        cogs_dir = os.path.join(os.path.dirname(__file__), 'cogs')
        
        logger.info(f"Chargement des cogs depuis: {cogs_dir}")
        
        # Vérifier que le dossier existe
        if not os.path.exists(cogs_dir):
            logger.error(f"Le dossier cogs n'existe pas: {cogs_dir}")
            return
        
        for filename in os.listdir(cogs_dir):
            if filename.endswith('.py') and filename != '__init__.py':
                cog_name = filename[:-3]
                try:
                    await self.load_extension(f'cogs.{cog_name}')
                    logger.info(f"✅ Cog chargé: {cog_name}")
                except Exception as e:
                    logger.error(f"❌ Erreur lors du chargement de {cog_name}: {e}")
    
    async def on_ready(self):
        """Événement déclenché quand le bot est connecté"""
        logger.info(f"🎮 {self.user} est connecté!")
        logger.info(f"📊 {len(self.guilds)} serveur(s) rejoints")
        
        # Synchroniser les commandes slash
        try:
            synced = await self.tree.sync()
            logger.info(f"✅ {len(synced)} commande(s) slash synchronisée(s)")
        except Exception as e:
            logger.error(f"❌ Erreur lors de la synchronisation: {e}")
        except Exception as e:
            print(f"❌ Erreur lors de la synchronisation: {e}")


def main():
    """Fonction principale"""
    bot = VolleyBot()
    
    @bot.event
    async def on_app_command_error(interaction: discord.Interaction, error: discord.app_commands.AppCommandError):
        """Gestion des erreurs des commandes slash"""
        if isinstance(error, discord.app_commands.MissingPermissions):
            await interaction.response.send_message("❌ Vous n'avez pas la permission d'utiliser cette commande.", ephemeral=True)
        else:
            await interaction.response.send_message(f"❌ Une erreur est survenue: {error}", ephemeral=True)
    
    # Démarrer le bot
    try:
        bot.run(DISCORD_TOKEN)
    except discord.errors.LoginFailure:
        logger.error("❌ Erreur de connexion: Token Discord invalide!")
    except Exception as e:
        logger.error(f"❌ Erreur lors du démarrage du bot: {e}")


if __name__ == "__main__":
    main()
