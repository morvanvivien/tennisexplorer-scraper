"""Minimal example: run the tennisexplorer-scraper Actor and print the results.

Usage: APIFY_TOKEN=... python run.py   (pip install apify-client)
"""
import os
import sys

from apify_client import ApifyClient

token = os.environ.get("APIFY_TOKEN")
if not token:
    sys.exit("Set the APIFY_TOKEN environment variable first.")

client = ApifyClient(token)

run_input = {
    "type": "atp-single",
    "mode": "results",
    "days": 3,
    "maxItems": 50,
}

run = client.actor("bibian/tennisexplorer-scraper").call(run_input=run_input)

count = 0
for item in client.dataset(run.default_dataset_id).iterate_items():
    count += 1
    print(f"{item['tournament']} | {item['player1']} vs {item['player2']} | {item.get('resultPlayer1')}-{item.get('resultPlayer2')}")
print(f"{count} results")
