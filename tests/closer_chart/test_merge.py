from fantasy_baseball.closer_chart.merge import merge_data, process_closers, process_waivers


def test_merge(closer_teams, waivers):
    actual = merge_data(closer_teams, waivers)
    expected = [{
        "name": "Joe Kelly",
        "id": 31992,
        "link": "https://www.espn.com/mlb/player/_/id/31992/joe-kelly",
        "role": "Secondary setup",
        "team": "LOS ANGELES DODGERS",
        "owned": 1.5,
        "tired": True,
        "injury": "ACTIVE",
        "teamId": 19,
        "status": "WAIVERS"
    }]
    assert actual == expected

def test_process_closers(closer_teams):
    processed = process_closers(closer_teams)
    actual = [x for x in processed
              if x['name'] in ['Evan Phillips', 'Joe Kelly']]
    expected = [
        {
            'name': 'Evan Phillips',
            'id': 37911,
            'link': 'https://www.espn.com/mlb/player/_/id/37911/evan-phillips',
            'role': 'Closer',
            'team': 'LOS ANGELES DODGERS',
            'owned': 86.9,
            'tired': False
        }, {
            'name': 'Joe Kelly',
            'id': 31992,
            'link': 'https://www.espn.com/mlb/player/_/id/31992/joe-kelly',
            'role': 'Secondary setup',
            'team': 'LOS ANGELES DODGERS',
            'owned': 1.5,
            'tired': True
        }
    ]
    assert actual == expected

def test_process_available_players(waivers):
    actual = process_waivers(waivers=waivers)
    expected = {
        31992: {
            'id': 31992,
            'name': 'Joe Kelly',
            'injury': 'ACTIVE',
            'teamId': 19,
            'status': 'WAIVERS',
        }
    }
    assert actual == expected
