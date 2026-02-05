"""
Module pour les appels API Volleyball
"""

import aiohttp
import asyncio
from config import VOLLEYBALL_API_KEY, VOLLEYBALL_API_BASE_URL


class VolleyballAPI:
    """Classe pour gérer les appels API Volleyball"""
    
    def __init__(self):
        self.base_url = VOLLEYBALL_API_BASE_URL
        self.api_key = VOLLEYBALL_API_KEY
        self.headers = {
            "x-apisports-key": self.api_key
        }
    
    async def get_team_ranking(self, team_name: str) -> dict:
        """
        Récupère le classement d'une équipe
        """
        try:
            async with aiohttp.ClientSession() as session:
                # Récupérer les équipes pour trouver l'ID
                teams = await self._get_teams(session)
                
                # Chercher l'équipe par nom
                team_id = None
                for team in teams:
                    if team_name.lower() in team.get('name', '').lower():
                        team_id = team.get('id')
                        break
                
                if not team_id:
                    return {
                        'success': False,
                        'message': f"Équipe '{team_name}' non trouvée"
                    }
                
                # Récupérer le classement
                url = f"{self.base_url}/standings"
                params = {
                    'team': team_id,
                    'season': 2024
                }
                
                async with session.get(url, headers=self.headers, params=params) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        return {
                            'success': True,
                            'data': data
                        }
                    else:
                        return {
                            'success': False,
                            'message': f"Erreur API: {resp.status}"
                        }
        except Exception as e:
            return {
                'success': False,
                'message': f"Erreur: {str(e)}"
            }
    
    async def get_daily_matches(self, country: str) -> dict:
        """
        Récupère les matchs du jour pour un pays
        """
        try:
            async with aiohttp.ClientSession() as session:
                # Récupérer le pays pour obtenir l'ID
                leagues = await self._get_leagues(session)
                
                country_id = None
                country_name = None
                for league in leagues:
                    country_field = league.get('country')
                    if isinstance(country_field, dict):
                        league_country = country_field.get('name', '')
                    else:
                        league_country = country_field or ''

                    if country.lower() in str(league_country).lower():
                        country_id = league.get('id')
                        country_name = league_country
                        break
                
                if not country_id:
                    return {
                        'success': False,
                        'message': f"Pays '{country}' non trouvé"
                    }
                
                # Récupérer les matchs du jour
                url = f"{self.base_url}/matches"
                params = {
                    'league': country_id,
                    'date': 'now'
                }
                
                async with session.get(url, headers=self.headers, params=params) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        return {
                            'success': True,
                            'country': country_name,
                            'data': data
                        }
                    else:
                        return {
                            'success': False,
                            'message': f"Erreur API: {resp.status}"
                        }
        except Exception as e:
            return {
                'success': False,
                'message': f"Erreur: {str(e)}"
            }
    
    async def get_match_score(self, team_name: str) -> dict:
        """
        Récupère le score des matchs pour une équipe
        """
        try:
            async with aiohttp.ClientSession() as session:
                # Récupérer les équipes
                teams = await self._get_teams(session)
                
                # Chercher l'équipe par nom
                team_id = None
                found_team_name = None
                for team in teams:
                    if team_name.lower() in team.get('name', '').lower():
                        team_id = team.get('id')
                        found_team_name = team.get('name')
                        break
                
                if not team_id:
                    return {
                        'success': False,
                        'message': f"Équipe '{team_name}' non trouvée"
                    }
                
                # Récupérer les matchs de l'équipe
                url = f"{self.base_url}/matches"
                params = {
                    'team': team_id,
                    'last': 5
                }
                
                async with session.get(url, headers=self.headers, params=params) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        return {
                            'success': True,
                            'team': found_team_name,
                            'data': data
                        }
                    else:
                        return {
                            'success': False,
                            'message': f"Erreur API: {resp.status}"
                        }
        except Exception as e:
            return {
                'success': False,
                'message': f"Erreur: {str(e)}"
            }
    
    async def _get_teams(self, session: aiohttp.ClientSession) -> list:
        """Récupère la liste des équipes"""
        try:
            url = f"{self.base_url}/teams"
            async with session.get(url, headers=self.headers) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    return data.get('response', [])
                return []
        except Exception as e:
            print(f"Erreur lors de la récupération des équipes: {e}")
            return []
    
    async def _get_leagues(self, session: aiohttp.ClientSession) -> list:
        """Récupère la liste des ligues/pays"""
        try:
            url = f"{self.base_url}/leagues"
            async with session.get(url, headers=self.headers) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    return data.get('response', [])
                return []
        except Exception as e:
            print(f"Erreur lors de la récupération des ligues: {e}")
            return []
