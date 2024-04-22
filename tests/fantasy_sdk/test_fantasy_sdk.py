from pytest import mark
import json

from fantasy_baseball.espn_sdk import Player
from test_utils.path_anchor import TEST_DIR

@mark.espn_integration
def test_get_available_relief_pitchers(sdk):
    players = list(sdk.get_available_relief_pitchers(n_pages=2, page_size=25))
    assert len(players) == 50

def test_deserialize_player():
    with open(TEST_DIR / 'michael_king.json') as f:
        player_json = f.read()
    player_dict_expected = json.loads(player_json)
    player = Player.from_json(player_json)
    # serialize & deserialize again to force all int keys to be converted to str
    player_dict_actual = json.loads(json.dumps(player.to_dict()))
    assert player_dict_actual == player_dict_expected
