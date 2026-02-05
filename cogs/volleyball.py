"""
Cog pour les commandes Volleyball du bot Discord
"""

import discord
from discord import app_commands
from discord.ext import commands
from utils.api import VolleyballAPI
from datetime import datetime


class VolleyballCog(commands.Cog):
    """Cog contenant les commandes Volleyball"""
    
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.api = VolleyballAPI()
    
    @app_commands.command(
        name="volleybot",
        description="Commandes VolleyBot pour consulter les infos volley"
    )
    @app_commands.describe(
        action="Action: 'classement' (équipe), 'matchs' (pays), ou 'score' (équipe)",
        parametre="Nom de l'équipe ou du pays"
    )
    async def volleybot(
        self,
        interaction: discord.Interaction,
        action: str,
        parametre: str
    ):
        """Commande principale VolleyBot"""
        
        await interaction.response.defer()
        
        try:
            if action.lower() == "classement":
                await self._handle_ranking(interaction, parametre)
            elif action.lower() == "matchs":
                await self._handle_matches(interaction, parametre)
            elif action.lower() == "score":
                await self._handle_score(interaction, parametre)
            else:
                embed = discord.Embed(
                    title="❌ Action invalide",
                    description="Les actions disponibles sont:\n"
                               "• **classement** [équipe] - Affiche le classement d'une équipe\n"
                               "• **matchs** [pays] - Affiche les matchs du jour\n"
                               "• **score** [équipe] - Affiche les scores récents",
                    color=discord.Color.red()
                )
                await interaction.followup.send(embed=embed)
        except Exception as e:
            embed = discord.Embed(
                title="❌ Erreur",
                description=f"Une erreur est survenue: {str(e)}",
                color=discord.Color.red()
            )
            await interaction.followup.send(embed=embed)
    
    async def _handle_ranking(self, interaction: discord.Interaction, team_name: str):
        """Affiche le classement d'une équipe"""
        result = await self.api.get_team_ranking(team_name)
        
        if not result['success']:
            embed = discord.Embed(
                title="❌ Erreur",
                description=result['message'],
                color=discord.Color.red()
            )
            await interaction.followup.send(embed=embed)
            return
        
        try:
            data = result['data'].get('response', [])
            if not data:
                embed = discord.Embed(
                    title="❌ Aucune donnée",
                    description=f"Aucune donnée de classement trouvée pour '{team_name}'",
                    color=discord.Color.red()
                )
                await interaction.followup.send(embed=embed)
                return
            
            standings = data[0].get('standings', [])
            if not standings:
                embed = discord.Embed(
                    title="❌ Aucune donnée",
                    description="Aucune donnée de classement disponible",
                    color=discord.Color.red()
                )
                await interaction.followup.send(embed=embed)
                return
            
            teams_data = standings[0].get('teams', [])
            
            # Trouver notre équipe
            our_team = None
            for team in teams_data:
                if team_name.lower() in team.get('team', {}).get('name', '').lower():
                    our_team = team
                    break
            
            if not our_team:
                embed = discord.Embed(
                    title="❌ Équipe non trouvée",
                    description=f"Équipe '{team_name}' non trouvée dans le classement",
                    color=discord.Color.red()
                )
                await interaction.followup.send(embed=embed)
                return
            
            # Créer l'embed
            team_name_full = our_team.get('team', {}).get('name', team_name)
            embed = discord.Embed(
                title=f"🏐 Classement - {team_name_full}",
                color=discord.Color.blue()
            )
            
            embed.add_field(
                name="Position",
                value=str(our_team.get('position', 'N/A')),
                inline=True
            )
            embed.add_field(
                name="Points",
                value=str(our_team.get('points', 'N/A')),
                inline=True
            )
            embed.add_field(
                name="Matchs joués",
                value=str(our_team.get('p', 'N/A')),
                inline=True
            )
            embed.add_field(
                name="Victoires",
                value=str(our_team.get('w', 'N/A')),
                inline=True
            )
            embed.add_field(
                name="Défaites",
                value=str(our_team.get('l', 'N/A')),
                inline=True
            )
            embed.add_field(
                name="Ratio points",
                value=f"{our_team.get('pf', 'N/A')} - {our_team.get('pa', 'N/A')}",
                inline=True
            )
            
            embed.set_footer(text=f"Mis à jour: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
            
            await interaction.followup.send(embed=embed)
        except Exception as e:
            embed = discord.Embed(
                title="❌ Erreur lors du traitement",
                description=f"Erreur: {str(e)}",
                color=discord.Color.red()
            )
            await interaction.followup.send(embed=embed)
    
    async def _handle_matches(self, interaction: discord.Interaction, country: str):
        """Affiche les matchs du jour pour un pays"""
        result = await self.api.get_daily_matches(country)
        
        if not result['success']:
            embed = discord.Embed(
                title="❌ Erreur",
                description=result['message'],
                color=discord.Color.red()
            )
            await interaction.followup.send(embed=embed)
            return
        
        try:
            matches = result['data'].get('response', [])
            country_name = result.get('country', country)
            
            if not matches:
                embed = discord.Embed(
                    title=f"📅 Matchs du jour - {country_name}",
                    description="Aucun match programmé pour aujourd'hui",
                    color=discord.Color.orange()
                )
                await interaction.followup.send(embed=embed)
                return
            
            embed = discord.Embed(
                title=f"📅 Matchs du jour - {country_name}",
                color=discord.Color.green(),
                description=f"Total: {len(matches)} match(s)"
            )
            
            for match in matches[:10]:  # Limiter à 10 matchs
                home_team = match.get('teams', {}).get('home', {}).get('name', 'Équipe 1')
                away_team = match.get('teams', {}).get('away', {}).get('name', 'Équipe 2')
                date = match.get('date', 'Date inconnue')
                status = match.get('status', 'Planifié')
                
                score_home = match.get('scores', {}).get('home', '-')
                score_away = match.get('scores', {}).get('away', '-')
                
                match_info = f"{home_team} **{score_home}** vs **{score_away}** {away_team}\n"
                match_info += f"⏰ {date} • Status: {status}"
                
                embed.add_field(
                    name=f"{home_team} vs {away_team}",
                    value=match_info,
                    inline=False
                )
            
            embed.set_footer(text=f"Mis à jour: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
            
            await interaction.followup.send(embed=embed)
        except Exception as e:
            embed = discord.Embed(
                title="❌ Erreur lors du traitement",
                description=f"Erreur: {str(e)}",
                color=discord.Color.red()
            )
            await interaction.followup.send(embed=embed)
    
    async def _handle_score(self, interaction: discord.Interaction, team_name: str):
        """Affiche les scores récents d'une équipe"""
        result = await self.api.get_match_score(team_name)
        
        if not result['success']:
            embed = discord.Embed(
                title="❌ Erreur",
                description=result['message'],
                color=discord.Color.red()
            )
            await interaction.followup.send(embed=embed)
            return
        
        try:
            matches = result['data'].get('response', [])
            team_name_full = result.get('team', team_name)
            
            if not matches:
                embed = discord.Embed(
                    title=f"⚽ Scores - {team_name_full}",
                    description="Aucun match trouvé",
                    color=discord.Color.red()
                )
                await interaction.followup.send(embed=embed)
                return
            
            embed = discord.Embed(
                title=f"⚽ Scores récents - {team_name_full}",
                color=discord.Color.purple(),
                description=f"Total: {len(matches)} dernier(s) match(s)"
            )
            
            for match in matches:
                home_team = match.get('teams', {}).get('home', {}).get('name', 'Équipe 1')
                away_team = match.get('teams', {}).get('away', {}).get('name', 'Équipe 2')
                date = match.get('date', 'Date inconnue')
                status = match.get('status', 'Fini')
                
                score_home = match.get('scores', {}).get('home', '-')
                score_away = match.get('scores', {}).get('away', '-')
                
                # Déterminer le résultat pour notre équipe
                result_str = ""
                if team_name_full.lower() in home_team.lower():
                    if score_home > score_away:
                        result_str = "✅ Victoire"
                    elif score_home < score_away:
                        result_str = "❌ Défaite"
                    else:
                        result_str = "🟡 Égalité"
                elif team_name_full.lower() in away_team.lower():
                    if score_away > score_home:
                        result_str = "✅ Victoire"
                    elif score_away < score_home:
                        result_str = "❌ Défaite"
                    else:
                        result_str = "🟡 Égalité"
                
                match_info = f"{home_team} **{score_home}** vs **{score_away}** {away_team}\n"
                match_info += f"⏰ {date} • {result_str}"
                
                embed.add_field(
                    name=f"{home_team} vs {away_team}",
                    value=match_info,
                    inline=False
                )
            
            embed.set_footer(text=f"Mis à jour: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
            
            await interaction.followup.send(embed=embed)
        except Exception as e:
            embed = discord.Embed(
                title="❌ Erreur lors du traitement",
                description=f"Erreur: {str(e)}",
                color=discord.Color.red()
            )
            await interaction.followup.send(embed=embed)


async def setup(bot: commands.Bot):
    """Charge le cog dans le bot"""
    await bot.add_cog(VolleyballCog(bot))
