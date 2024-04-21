from typing import List

import requests
import json
import time
import datetime
import random

from . import Player

LEAGUE_ID = 192574
THIS_YEAR = datetime.date.today().year

class ESPNFantasyBaseballSDK:

    def __init__(self, cookies, season_year=THIS_YEAR, league_id=LEAGUE_ID):
        self.cookies = self._serialize_cookies(cookies)
        self.season_year = season_year
        self.league_id = league_id

        self.session = requests.Session()
        serialized_cookies = self._serialize_cookies(cookies)
        self.session.cookies.update(serialized_cookies)
        self.session.headers = self._base_headers()

    @classmethod
    def _serialize_cookies(cls, cookies):
        # the value of 'espnAuth' is a JSON string, this is intentional!
        espn_auth = json.dumps({
            'swid': cookies['SWID']
        })
        return {**cookies, 'espnAuth': espn_auth}

    def _base_headers(self):
        return {
            'x-fantasy-platform': 'kona-PROD-755f3bd3193ffc4774c96674887e57efb4b3ce86',
            'x-fantasy-source': 'kona',
            'referer': f'https://fantasy.espn.com/baseball/players/add?leagueId={self.league_id}',
        }

    def get_available_relief_pitchers(self, n_pages, page_size=50) -> List[Player]:
        for page in self._generate_pages(n_pages, page_size):
            for player in page:
                yield player

    def _generate_pages(self, n_pages, page_size):
        is_first_page = True
        for page_number in range(n_pages):
            if not is_first_page:
                # wait 1-2 seconds, but randomized to avoid appearing programmatic
                time.sleep(1 + random.randint(1, 1000) / 1000)
            is_first_page = False
            yield self._get_player_page(page_number, page_size)

    def _get_player_page(self, page_number, page_size) -> List[Player]:
        url = (f"https://fantasy.espn.com/apis/v3/games/flb/"
               f"seasons/{self.season_year}/segments/0/leagues/{self.league_id}"
               "?scoringPeriodId=9&view=kona_player_info")
        fantasy_filter = self._get_availability_filter(page_number, page_size)
        headers = self._get_fantasy_filter_headers(fantasy_filter)
        resp = self.session.get(url=url, headers=headers)
        players = resp.json().get('players')
        if not players:
            raise Exception("No available players found on waivers.")
        return [Player.from_dict(x, infer_missing=True) for x in players]

    # noinspection PyMethodMayBeStatic
    def _get_fantasy_filter_headers(self, fantasy_filter):
        return {
            'x-fantasy-filter': json.dumps(fantasy_filter)
        }

    # noinspection PyMethodMayBeStatic
    def _get_availability_filter(self, page_number, limit):
        offset = page_number * limit

        return {
            "players": {
                "filterStatus": {
                    "value": [
                        "FREEAGENT",
                        "WAIVERS",
                        # excluding ONTEAM option
                    ]
                },
                "filterSlotIds": {
                    "value": [
                        15
                    ]
                },
                "filterRanksForScoringPeriodIds": {
                    "value": [
                        9
                    ]
                },
                "limit": limit,
                "offset": offset,
                "sortPercOwned": {
                    "sortAsc": False,
                    "sortPriority": 1
                },
                "sortDraftRanks": {
                    "sortPriority": 100,
                    "sortAsc": True,
                    "value": "STANDARD"
                },
                "filterRanksForRankTypes": {
                    "value": [
                        "STANDARD"
                    ]
                },
                "filterStatsForTopScoringPeriodIds": {
                    "value": 5,
                    "additionalValue": [
                        "002022",
                        "102022",
                        "002021",
                        "012022",
                        "022022",
                        "032022",
                        "042022",
                        "062022",
                        "010002022"
                    ]
                }
            }
        }
