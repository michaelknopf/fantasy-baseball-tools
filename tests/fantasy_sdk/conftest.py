import json

from pytest import fixture

from sabr import path_anchor
from sabr.fantasy_sdk import ESPNFantasyBaseballSDK

@fixture
def sdk():
    config_path = path_anchor.CONFIG_DIR / 'config.json'
    if not config_path.exists():
        raise Exception(f"Config not found at {config_path}")

    with open(config_path) as f:
        config = json.load(f)
        cookies = config['cookies']

    return ESPNFantasyBaseballSDK(cookies=cookies)
