from typing import List

from fantasy_baseball.espn_sdk import Player
from fantasy_baseball.closer_chart import CloserChartTeam


MERGED_FIELDS = ['name', 'role', 'id', 'injury', 'status', 'tired', 'owned', 'link']

def merge_data(closer_teams: List[CloserChartTeam],
               waivers: List[Player]):
    """
    Merge list of pitchers from
        1) ESPN Closer Chart
        2) Free Agent list in an ESPN fantasy league
    """
    waiver_rows = process_waivers(waivers)
    closers = process_closers(closer_teams)
    merged = []
    for closer in closers:
        player_id = closer['id']
        player = waiver_rows.get(player_id)
        if player:
            merged.append({**closer, **player})
    return merged

def process_closers(closer_teams: List[CloserChartTeam]):
    """
    Each team has a list of closers. Turn this into a single list of all closers,
    with some team information denormalized onto each element. This also processes
    each closer element into a dictionary of fields we will need in the final CSV.
    """
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

def process_waivers(waivers: List[Player]):
    """
    Process each waiver player into columns for the CSV.
    Index the players in dictionary, by ID, for fast lookup.
    """
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
