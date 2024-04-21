from typing import List

from sabr.fantasy_sdk import Player
from sabr.closer_chart import CloserChartTeam

def merge_data(closer_teams: List[CloserChartTeam], waivers: List[Player]):
    waiver_rows = index_waivers(waivers)
    closers = flatten_closers(closer_teams)
    merged = []
    for closer in closers:
        player_id = closer['id']
        waiver = waiver_rows.get(player_id)
        if waiver:
            merged.append({**closer, **waiver})
    return merged

def flatten_closers(closer_teams: List[CloserChartTeam]):
    rows = []
    for team in closer_teams:
        for pitcher in team.pitchers:
            row = {
                'name': pitcher.name,
                'id': pitcher.id,
                'link': pitcher.link,
                'role': pitcher.role,
                'team': team.name,
                'owned': pitcher.ownership_percentage,
                'tired': pitcher.is_tired,
            }
            rows.append(row)
    return rows

def index_waivers(waivers: List[Player]):
    rows = {}
    for p in waivers:
        row = {
            'id': p.id,
            'name': p.player.full_name,
            'injury': p.player.injury_status,
            'teamId': p.player.pro_team_id,
            # 'onTeamId': p['onTeamId'],
            'status': p.status
        }
        rows[p.id] = row
    return rows
