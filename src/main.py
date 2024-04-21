from sabr.fantasy_sdk import ESPNFantasyBaseballSDK, Player
from sabr.closer_chart import parse_closer_chart, merge, CloserChartTeam
from sabr.path_anchor import DATA_DIR, CONFIG_DIR

import json
import os
import datetime
import csv

DATE = datetime.datetime.now().strftime("%y_%m_%d")
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
RUNS_DIR = DATA_DIR / 'closer_chart_runs' / DATE

CLOSER_CHART_FILE = RUNS_DIR / "closer_chart.json"
WAIVERS_FILE = RUNS_DIR / "waivers.json"
MERGED_FILE = RUNS_DIR / "merged.json"
MERGED_CSV_FILE = RUNS_DIR / f"{DATE}.csv"

RUNS_DIR.mkdir(parents=True, exist_ok=True)

if not CLOSER_CHART_FILE.exists():
    print("Pulling closer chart...")
    closer_teams = parse_closer_chart.get_closers()
    with open(CLOSER_CHART_FILE, 'w') as f:
        json.dump([x.to_dict() for x in closer_teams], f, indent=2)
else:
    print(f"Closer chart cached: {CLOSER_CHART_FILE}")

if not WAIVERS_FILE.exists():
    print("Pulling waivers...")
    with open(CONFIG_DIR / "config.json") as f:
        config = json.load(f)
        cookies = config.get('cookies', {})
    fantasy = ESPNFantasyBaseballSDK(cookies)
    waivers = fantasy.get_available_relief_pitchers(2)
    with open(WAIVERS_FILE, 'w') as f:
        json.dump([x.to_dict() for x in waivers], f, indent=2)
else:
    print(f"Waivers cached: {WAIVERS_FILE}")

with open(CLOSER_CHART_FILE) as f:
    closer_teams_dict = json.load(f)
closer_teams = [CloserChartTeam.from_dict(x, infer_missing=True) for x in closer_teams_dict]

with open(WAIVERS_FILE) as f:
    waivers_dicts = json.load(f)
waivers = [Player.from_dict(x, infer_missing=True) for x in waivers_dicts]

with open(MERGED_FILE, 'w') as f:
    merged = merge.merge_data(closer_teams, waivers)
    json.dump(merged, f, indent=2)

field_names = ['name', 'role', 'id', 'injury', 'status', 'tired', 'owned', 'link']
with open(MERGED_CSV_FILE, 'w') as csvfile:
    print("Merging closers with waivers...")
    writer = csv.DictWriter(csvfile, fieldnames=field_names, extrasaction='ignore')
    writer.writeheader()
    writer.writerows(merged)

print(f"Output: {MERGED_CSV_FILE}")

