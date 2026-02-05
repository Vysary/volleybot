"""
Module pour les appels API Volleyball
"""

import aiohttp
import asyncio
import logging
from datetime import datetime
from config import VOLLEYBALL_API_KEY, VOLLEYBALL_API_BASE_URL

logger = logging.getLogger('VolleyballAPI')


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
                teams = await self._search_teams(session, team_name)
                if not teams:
                    teams = await self._get_teams(session)
                
                # Chercher l'équipe par nom
                team_id = None
                found_team_name = None
                for team in teams:
                    team_obj = team.get('team', team)
                    team_name_value = team_obj.get('name', '')
                    if team_name.lower() in str(team_name_value).lower():
                        team_id = team_obj.get('id') or team.get('id')
                        found_team_name = team_name_value
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
                }data = await resp.json()
                    logger.info(f"API standings réponse: {data}")
                    if resp.status == 200:
                async with session.get(url, headers=self.headers, params=params) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        return {
                            'success': True,
                            'team': found_team_name or team_name,
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
                
                matching_leagues = []
                country_name = None
                for league in leagues:
                    country_field = league.get('country')
                    if isinstance(country_field, dict):
                        league_country = country_field.get('name', '')
                    else:
                        league_country = country_field or ''

                    if country.lower() in str(league_country).lower():
                        league_id = league.get('id') or league.get('league', {}).get('id')
                        if league_id:
                            matching_leagues.append(league_id)
                            country_name = league_country
                
                if not matching_leagues:
                    return {
                        'success': False,
                        'message': f"Pays '{country}' non trouvé"
                    }
                
                # Récupérer les matchs du jour
                logger.info(f"Recherche matchs pour {country} (leagues: {matching_leagues}) à la date {date_str}")
                all_matches = []
                for league_id in matching_leagues[:5]:  # limiter pour éviter trop d'appels
                    params = {
                        'league': league_id,
                        'date': date_str
                    }
                    data = await self._fetch_games(session, params)
                    logger.info(f"Réponse /games pour ligue {league_id}: {data}")
                    if data is None:
                        data = await self._fetch_matches(session, params)
                        logger.info(f"Réponse /matches pour ligue {league_id}: {data}")
                    if data and data.get('response'):
                        all_matches.extend(data.get('response', []))
                
                logger.info(f"Total matchs trouvés: {len(all_matches)}")        all_matches.extend(data.get('response', []))
                
                return {
                    'success': True,
                    'country': country_name or country,
                    'data': {'response': all_matches}
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
                teams = await self._search_teams(session, team_name)
                if not teams:
                    teams = await self._get_teams(session)
                
                # Chercher l'équipe par nom
                team_id = None
                found_team_name = None
                for team in teams:
                    team_obj = team.get('team', team)
                    team_name_value = team_obj.get('name', '')
                    if team_name.lower() in str(team_name_value).lower():
                        team_id = team_obj.get('id') or team.get('id')
                        found_team_name = team_name_value
                        break
                
                if not team_id:
                    return {
                        'success': False,
                        'message': f"Équipe '{team_name}' non trouvée"
                    }
                
                # Récupérer les matchs de l'équipe
                params = {
                    'team': team_id,
                    'last': 5
                }
                
                data = await self._fetch_games(session, params)
                if data is None:
                    data = await self._fetch_matches(session, params)
                if data is not None:
                    return {
                        'success': True,
                        'team': found_team_name or team_name,
                        'data': data
                    }
                else:
                    return {
                        'success': False,
                        'message': "Erreur API: impossible de récupérer les matchs"
                    }
        except Exception as e:
            return {
                'success': False,
                'message': f"Erreur: {str(e)}"
            }

    async def _fetch_games(self, session: aiohttp.ClientSession, params: dict) -> dict | None:
        """Récupère les matchs via l'endpoint /games"""
        try:
            url = f"{self.base_url}/games"
            async with session.get(url, headers=self.headers, params=params) as resp:
                if resp.status == 200:
                    return await resp.json()
                return None
        except Exception:
            return None

    async def _fetch_matches(self, session: aiohttp.ClientSession, params: dict) -> dict | None:
        """Fallback si l'endpoint /matches est utilisé"""
        try:
            url = f"{self.base_url}/matches"
            async with session.get(url, headers=self.headers, params=params) as resp:
                if resp.status == 200:
                    return await resp.json()
                return None
        except Exception:
            return None
    
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

    async def _search_teams(self, session: aiohttp.ClientSession, team_name: str) -> list:
        """Recherche une équipe par nom (si l'API supporte search)"""
        try:
            url = f"{self.base_url}/teams"
            params = {'search': team_name}
            async with session.get(url, headers=self.headers, params=params) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    return data.get('response', [])
                return []
        except Exception:
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
