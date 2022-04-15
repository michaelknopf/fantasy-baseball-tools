from sabr import parse_closer_chart, fantasy, merge
import json
import os
import datetime
import csv

DATE = datetime.datetime.now().strftime("%m_%d")
ROOT_DIR = d = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = f"{ROOT_DIR}/data/{DATE}"

CLOSER_CHART_FILE = os.path.join(DATA_DIR, "closer_chart.json")
WAIVERS_FILE = os.path.join(DATA_DIR, "waivers.json")
MERGED_FILE = os.path.join(DATA_DIR, "merged.json")
MERGED_CSV_FILE = os.path.join(DATA_DIR, "merged.csv")

if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

if not os.path.exists(CLOSER_CHART_FILE):
    closers = parse_closer_chart.get_closers()
    with open(CLOSER_CHART_FILE, 'w') as f:
        json.dump(closers, f, indent=2)

if not os.path.exists(WAIVERS_FILE):
    with open(os.path.join(ROOT_DIR, "config", "config.json")) as f:
        config = json.load(f)
        cookies = config.get('cookies', {})
    fantasy = fantasy.Fantasy(cookies)
    waivers = fantasy.get_players()
    with open(WAIVERS_FILE, 'w') as f:
        json.dump(waivers, f, indent=2)

with open(CLOSER_CHART_FILE) as f:
    closers = json.load(f)

with open(WAIVERS_FILE) as f:
    waivers = json.load(f)

with open(MERGED_FILE, 'w') as f:
    merged = merge.merge_data(closers, waivers)
    json.dump(merged, f, indent=2)

field_names = ['name', 'role', 'id', 'injury', 'status', 'link']
with open(MERGED_CSV_FILE, 'w') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=field_names, extrasaction='ignore')
    writer.writeheader()
    writer.writerows(merged)
