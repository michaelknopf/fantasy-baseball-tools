import json

def merge_data(closer_chart, waivers):
    waiver_rows = index_waivers(waivers)
    closers = flatten_closers(closer_chart)
    merged = []
    for closer in closers:
        player_id = closer['id']
        waiver = waiver_rows.get(player_id)
        if not waiver:
            waiver = {}
        else:
            merged.append({**closer, **waiver})
    return merged

def flatten_closers(closer_chart):
    closers = []
    for closer in closer_chart['closer']:
        closer['role'] = 'closer'
        closer['id'] = parse_closer_id(closer)
        closers.append(closer)
    for closer in closer_chart['setup']:
        closer['role'] = 'setup'
        closer['id'] = parse_closer_id(closer)
        closers.append(closer)
    return closers

def parse_closer_id(closer):
    # http://espn.go.com/mlb/player/_/id/33833/jorge-lopez
    closer_link = closer['link']
    prefix = "http://espn.go.com/mlb/player/_/id/"
    suffix = closer_link[len(prefix):]
    closer_id = suffix.split('/')[0]
    return int(closer_id)

def index_waivers(waivers):
    rows = {}
    for p in waivers:
        player_id = p['id']
        player = p['player']
        row = {
            'id': player_id,
            'name': player['fullName'],
            'injury': player['injuryStatus'],
            'teamId': player['proTeamId'],
            'onTeamId': p['onTeamId'],
            'status': p['status']
        }
        rows[player_id] = row
    return rows
