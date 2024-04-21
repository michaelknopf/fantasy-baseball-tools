from typing import Iterable, List

import requests
from bs4 import BeautifulSoup, Tag, ResultSet
import re

from sabr.closer_chart import CloserChartPitcher, CloserChartTeam

CLOSER_CHART_URL = "https://www.espn.com/fantasy/baseball/flb/story?page=REcloserorgchart"
USER_AGENT = ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
              'AppleWebKit/537.36 (KHTML, like Gecko) '
              'Chrome/124.0.0.0 Safari/537.36')

def get_closers() -> List[CloserChartTeam]:
    soup = get_closer_soup()
    return parse_closer_soup(soup)

def get_closer_html():
    resp = requests.get(CLOSER_CHART_URL,
                        headers={'User-Agent': USER_AGENT})
    return resp.content

def get_closer_soup(html=None):
    if not html:
        html = get_closer_html()
    return BeautifulSoup(html, 'html.parser')

def parse_closer_soup(soup: BeautifulSoup) -> List[CloserChartTeam]:
    main_section = soup.select('#article-feed > article:nth-child(1) > div > div.article-body')
    if not main_section:
        raise Exception("Cannot find main section")
    main_section_tag = main_section[0]
    return list(parse_team_soups(main_section_tag))

def parse_team_soups(main_section: Tag) -> Iterable[CloserChartTeam]:
    for p in main_section.find_all(name='p'):
        team = parse_team_soup(p)
        if team:
            yield team

def parse_team_soup(p: Tag) -> CloserChartTeam:
    team_link_tags = p.find_all(name="a",
                                href=re.compile("/mlb/team"),
                                recursive=True)
    if len(team_link_tags) != 1:
        return None

    team_link_tag = team_link_tags[0]
    team_name = team_link_tag.string.strip()
    team_link = team_link_tag.get('href')

    players = p.find_all(name="a",
                         href=re.compile("/mlb/player"),
                         recursive=True)
    pitchers = [parse_player_soup(player) for player in players]

    return CloserChartTeam(name=team_name,
                           link=team_link,
                           pitchers=pitchers)

def parse_player_soup(player_soup: Tag):
    player_link = player_soup.get('href')
    player_name = player_soup.string.strip()

    parent: Tag = player_soup.parent
    if parent.name == 'i':
        player_root_node: Tag = parent.parent
        is_tired = True
        if not player_root_node.name == 'b':
            raise Exception(f'Unexpected italicized but not bolded pitcher:\n{player_soup.prettify()}')
    else:
        is_tired = False
        player_root_node = player_soup

    role_tag = player_root_node.find_previous_sibling('b')
    if not role_tag:
        raise Exception(f'No previous <b> sibling found for player:\n{player_root_node.prettify()}')
    role = role_tag.string.strip().strip(':')

    ownership_percentage = player_root_node.next_sibling.string.strip()
    PERCENT_REGEX = re.compile('\\(\\d+\\.\\d+%\\)')
    if not PERCENT_REGEX.fullmatch(ownership_percentage):
        raise Exception(f'Ownership percentage does not match expected pattern: {ownership_percentage}')
    ownership_percentage = ownership_percentage[1:-2]

    player_id = parse_closer_id(player_link)
    if not player_id:
        raise Exception(f'Could not parse player ID from link: {player_link}')

    return CloserChartPitcher(name=player_name,
                              id=player_id,
                              link=player_link,
                              role=role,
                              ownership_percentage=ownership_percentage,
                              is_tired=is_tired)

# http://espn.go.com/mlb/player/_/id/33833/jorge-lopez
# https://www.espn.com/mlb/player/_/id/41432/kevin-ginkel
LINK_REGEX = re.compile('/mlb/player/.*/id/(\\d+)/.*')

def parse_closer_id(link):
    match = LINK_REGEX.search(link)
    if not match:
        return None
    closer_id = match.group(1)
    return int(closer_id)
