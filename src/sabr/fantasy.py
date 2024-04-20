import requests
import json
import time
import random

url = "https://fantasy.espn.com/apis/v3/games/flb/seasons/2022/segments/0/leagues/192574?scoringPeriodId=9&view=kona_player_info"


class Fantasy:

    def __init__(self, cookies):
        espn_auth = '{"swid":"' + cookies['SWID'] + '"}'
        self.cookies = {**cookies, 'espnAuth': espn_auth}

    def get_players(self):
        players = []
        for page in self.generate_pages(2):
            players.extend(page)
            time.sleep(1 + random.randint(1, 1000) / 1000)
        return players

    def generate_pages(self, n_pages):
        for page_number in range(n_pages):
            yield self.get_player_page(page_number)

    def get_player_page(self, page_number):
        fantasy_filter = self.get_fantasy_filter(page_number)
        headers = self.get_headers(fantasy_filter)
        resp = requests.get(url=url, headers=headers, cookies=self.cookies)
        return resp.json().get('players', [])

    def get_headers(self, fantasy_filter):
        return {
            'x-fantasy-platform': 'kona-PROD-755f3bd3193ffc4774c96674887e57efb4b3ce86',
            'x-fantasy-source': 'kona',
            'referer': 'https://fantasy.espn.com/baseball/players/add?leagueId=192574',
            'x-fantasy-filter': json.dumps(fantasy_filter)
        }

    def get_fantasy_filter(self, page_number):
        limit = 50
        offset = page_number * limit

        return {
            "players": {
                "filterStatus": {
                    "value": [
                        "FREEAGENT",
                        "WAIVERS",
                        # ONTEAM
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




