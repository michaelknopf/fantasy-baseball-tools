from fantasy_baseball.espn_sdk import ESPNFantasyBaseballSDK, Player
from fantasy_baseball.closer_chart import parse_closer_chart, merge_data, CloserChartTeam, MERGED_FIELDS
from fantasy_baseball.path_anchor import DATA_DIR, CONFIG_DIR

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

# pull and cache closer chart data for today
if not CLOSER_CHART_FILE.exists():
    print("Pulling closer chart...")
    closer_teams = parse_closer_chart.get_closers()
    with open(CLOSER_CHART_FILE, 'w') as f:
        json.dump([x.to_dict() for x in closer_teams], f, indent=2)
else:
    print(f"Loading cached closer chart: {CLOSER_CHART_FILE}")
    with open(CLOSER_CHART_FILE) as f:
        closer_teams_dict = json.load(f)
    closer_teams = [CloserChartTeam.from_dict(x, infer_missing=True) for x in closer_teams_dict]

# pull and cache waiver data for today
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
    print(f"Loading cached waivers: {WAIVERS_FILE}")
    with open(WAIVERS_FILE) as f:
        waivers_dicts = json.load(f)
    waivers = [Player.from_dict(x, infer_missing=True) for x in waivers_dicts]

# merge closer chart with waiver data
# dump merged result to CSV
merged = merge_data(closer_teams, waivers)
with open(MERGED_CSV_FILE, 'w') as csvfile:
    print("Merging closers with waivers...")
    writer = csv.DictWriter(csvfile, fieldnames=MERGED_FIELDS, extrasaction='ignore')
    writer.writeheader()
    writer.writerows(merged)

print(f"Merged results written to CSV: {MERGED_CSV_FILE}")
