from pytest import fixture
from bs4 import BeautifulSoup
import json

from fantasy_baseball.closer_chart import parse_closer_chart, CloserChartTeam
from fantasy_baseball.espn_sdk import Player
from test_utils.path_anchor import TEST_DIR

@fixture
def closer_chart_soup():
    path = TEST_DIR / 'closer_chart.html'
    if path.exists():
        # use cached file, if present
        with open(path) as f:
            html = f.read()
        return parse_closer_chart.get_closer_soup(html)
    else:
        # otherwise, download and cache
        html = parse_closer_chart.get_closer_html()
        html = html.decode('utf-8')
        soup = parse_closer_chart.get_closer_soup(html)

        # store in file cache for future tests
        with open(path, 'w') as f:
            f.write(soup.prettify())

        return soup

@fixture
def team_node_soup():
    with open(TEST_DIR / 'team_node.html') as f:
        html = f.read()
    return BeautifulSoup(html, 'html.parser')

@fixture
def closer_teams():
    with open(TEST_DIR / 'closer_teams.json') as f:
        closer_teams_json = json.load(f)
    return [CloserChartTeam.from_dict(x) for x in closer_teams_json]

@fixture
def waivers():
    with open(TEST_DIR / 'waivers.json') as f:
        players = json.load(f)
    return [Player.from_dict(x) for x in players]
