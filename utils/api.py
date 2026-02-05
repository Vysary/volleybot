"""
Module pour les appels API Volleyball
"""

import aiohttp
import asyncio
import logging
from datetime import datetime
from typing import Optional, List
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
        """Récupère le classement d'une équipe"""
        try:
            async with aiohttp.ClientSession() as session:
                logger.info(f"=== GET_TEAM_RANKING: {team_name} ===")
                teams = await self._search_teams(session, team_name)
                if not teams:
                    logger.info(f"DEBUG: Pas de résultats search, appel /teams sans filtre")
                    teams = await self._get_teams(session)
                
                logger.info(f"DEBUG: Total équipes à chercher: {len(teams)}")
                team_id = None
                found_team_name = None
                for team in teams:
                    team_obj = team.get('team', team)
                    team_name_value = team_obj.get('name', '')
                    logger.info(f"DEBUG: Vérification équipe: '{team_name_value}' vs '{team_name}'")
                    if team_name.lower() in str(team_name_value).lower():
                        team_id = team_obj.get('id') or team.get('id')
                        found_team_name = team_name_value
                        logger.info(f"DEBUG: ✅ MATCH trouvé! ID={team_id}")
                        break
                
                if not team_id:
                    logger.warning(f"Équipe '{team_name}' non trouvée après recherche")
                    return {'success': False, 'message': f"Équipe '{team_name}' non trouvée"}
                
                url = f"{self.base_url}/standings"
                params = {'team': team_id, 'season': 2024}
                logger.info(f"DEBUG: Appel standings avec team_id={team_id}")
                
                async with session.get(url, headers=self.headers, params=params) as resp:
                    data = await resp.json()
                    logger.info(f"Standings pour {team_name}: {resp.status}, response_count={len(data.get('response', []))}")
                    if resp.status == 200:
                        return {'success': True, 'team': found_team_name or team_name, 'data': data}
                    else:
                        return {'success': False, 'message': f"Erreur API: {resp.status}"}
        except Exception as e:
            logger.error(f"Erreur get_team_ranking: {e}")
            return {'success': False, 'message': f"Erreur: {str(e)}"}
    
    async def get_daily_matches(self, country: str) -> dict:
        """Récupère les matchs du jour pour un pays"""
        try:
            async with aiohttp.ClientSession() as session:
                logger.info(f"=== GET_DAILY_MATCHES: {country} ===")
                leagues = await self._get_leagues(session)
                logger.info(f"DEBUG: Total ligues chargées: {len(leagues)}")
                
                matching_leagues = []
                country_name = None
                for league in leagues:
                    country_field = league.get('country')
                    league_country = country_field.get('name', '') if isinstance(country_field, dict) else (country_field or '')
                    league_id = league.get('id') or league.get('league', {}).get('id')
                    logger.info(f"DEBUG: Ligue: pays='{league_country}', ID={league_id}")
                    
                    if country.lower() in str(league_country).lower():
                        if league_id:
                            matching_leagues.append(league_id)
                            country_name = league_country
                            logger.info(f"DEBUG: ✅ MATCH trouvé! Pays='{league_country}', ID={league_id}")
                
                if not matching_leagues:
                    logger.warning(f"Pays '{country}' non trouvé dans les ligues")
                    return {'success': False, 'message': f"Pays '{country}' non trouvé"}
                
                date_str = datetime.utcnow().strftime('%Y-%m-%d')
                logger.info(f"DEBUG: Recherche matchs {country} pour {len(matching_leagues)} ligues à {date_str}")
                all_matches = []
                for league_id in matching_leagues[:5]:
                    params = {'league': league_id, 'date': date_str}
                    data = await self._fetch_games(session, params)
                    if data:
                        matches_count = len(data.get('response', []))
                        logger.info(f"DEBUG: /games ligue {league_id}: {matches_count} matchs")
                        if matches_count > 0:
                            all_matches.extend(data.get('response', []))
                    else:
                        data = await self._fetch_matches(session, params)
                        if data:
                            matches_count = len(data.get('response', []))
                            logger.info(f"DEBUG: /matches ligue {league_id}: {matches_count} matchs")
                            if matches_count > 0:
                                all_matches.extend(data.get('response', []))
                
                logger.info(f"DEBUG: TOTAL matchs trouvés: {len(all_matches)}")
                return {'success': True, 'country': country_name or country, 'data': {'response': all_matches}}
        except Exception as e:
            logger.error(f"Erreur get_daily_matches: {e}")
            return {'success': False, 'message': f"Erreur: {str(e)}"}
    
    async def get_match_score(self, team_name: str) -> dict:
        """Récupère le score des matchs pour une équipe"""
        try:
            async with aiohttp.ClientSession() as session:
                teams = await self._search_teams(session, team_name)
                if not teams:
                    teams = await self._get_teams(session)
                
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
                    return {'success': False, 'message': f"Équipe '{team_name}' non trouvée"}
                
                params = {'team': team_id, 'last': 5}
                data = await self._fetch_games(session, params)
                if data is None:
                    data = await self._fetch_matches(session, params)
                if data is not None:
                    return {'success': True, 'team': found_team_name or team_name, 'data': data}
                else:
                    return {'success': False, 'message': "Erreur API"}
        except Exception as e:
            return {'success': False, 'message': f"Erreur: {str(e)}"}

    async def _fetch_games(self, session: aiohttp.ClientSession, params: dict) -> Optional[dict]:
        """Récupère via /games"""
        try:
            url = f"{self.base_url}/games"
            async with session.get(url, headers=self.headers, params=params) as resp:
                if resp.status == 200:
                    return await resp.json()
                return None
        except Exception:
            return None

    async def _fetch_matches(self, session: aiohttp.ClientSession, params: dict) -> Optional[dict]:
        """Fallback /matches"""
        try:
            url = f"{self.base_url}/matches"
            async with session.get(url, headers=self.headers, params=params) as resp:
                if resp.status == 200:
                    return await resp.json()
                return None
        except Exception:
            return None
    
    async def _get_teams(self, session: aiohttp.ClientSession) -> List[dict]:
        """Récupère les équipes"""
        try:
            url = f"{self.base_url}/teams"
            async with session.get(url, headers=self.headers) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    return data.get('response', [])
                return []
        except Exception as e:
            logger.error(f"Erreur _get_teams: {e}")
            return []

    async def _search_teams(self, session: aiohttp.ClientSession, team_name: str) -> List[dict]:
        """Recherche équipe par nom"""
        try:
            url = f"{self.base_url}/teams"
            params = {'search': team_name}
            logger.info(f"DEBUG: Appel /teams avec search='{team_name}'")
            async with session.get(url, headers=self.headers, params=params) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    teams = data.get('response', [])
                    logger.info(f"DEBUG: Réponse /teams search: {len(teams)} équipes trouvées")
                    if teams:
                        logger.info(f"DEBUG: Équipes trouvées: {[t.get('name') for t in teams]}")
                    return teams
                logger.warning(f"DEBUG: /teams search retourna {resp.status}")
                return []
        except Exception as e:
            logger.error(f"Erreur _search_teams: {e}")
            return []
    
    async def _get_leagues(self, session: aiohttp.ClientSession) -> List[dict]:
        """Récupère les ligues"""
        try:
            url = f"{self.base_url}/leagues"
            async with session.get(url, headers=self.headers) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    return data.get('response', [])
                return []
        except Exception as e:
            logger.error(f"Erreur _get_leagues: {e}")
