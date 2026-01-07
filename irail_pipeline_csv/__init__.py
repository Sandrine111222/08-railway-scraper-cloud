# irail_pipeline_csv.py
"""
iRail Data Pipeline
Features:
- Live Departure Board
- Delay Monitor
- Route Explorer
- Train Type Distribution
- Peak Hour Analysis
- Real-Time Train Map
Automation:
- Scheduled runs via Azure Functions Timer Trigger
- CSV outputs for live dashboards (Power BI, Excel)
"""

import os
import requests
import csv
from datetime import datetime
from pathlib import Path
import pandas as pd

# CONFIGURATION

# CSV storage folder (works locally or in Azure Function container)
DATA_DIR = Path(os.getenv("DATA_DIR", "./data"))
DATA_DIR.mkdir(exist_ok=True)

# Example stations/cities for live departures
STATIONS = ["Brussels-Central", "Antwerp-Central"]

# iRail API endpoints
API_BASE = "https://api.irail.be"


# FETCH DATA FUNCTIONS

def fetch_live_departures(station: str):
    """Fetch current departures for a station"""
    url = f"{API_BASE}/liveboard/?station={station}&format=json"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    departures = data.get("departures", {}).get("departure", [])
    return departures

# Example: Delay Monitor
def fetch_delay_monitor(station: str):
    """Extract delays for a station"""
    departures = fetch_live_departures(station)
    delay_data = []
    for dep in departures:
        delay = int(dep.get("delay", 0))
        train_type = dep.get("vehicle")
        time = dep.get("time")
        delay_data.append({
            "station": station,
            "train": train_type,
            "scheduled_time": datetime.fromtimestamp(int(time)),
            "delay": delay
        })
    return delay_data


# CSV WRITE FUNCTIONS

def save_to_csv(filename: str, data: list, fieldnames: list):
    """Save list of dicts to CSV"""
    filepath = DATA_DIR / filename
    file_exists = filepath.exists()
    with open(filepath, mode="a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        writer.writerows(data)


# MAIN PIPELINE

def run_pipeline():
    print("🔹 Starting iRail Pipeline...")
    for station in STATIONS:
        print(f"Fetching live departures for {station}...")
        departures = fetch_live_departures(station)
        # Save Live Departure Board
        if departures:
            save_to_csv("live_departures.csv", departures, fieldnames=departures[0].keys())
        
        # Save Delay Monitor
        delay_data = fetch_delay_monitor(station)
        if delay_data:
            save_to_csv("delay_monitor.csv", delay_data, fieldnames=delay_data[0].keys())

    print(f"✅ Pipeline completed. CSVs saved to {DATA_DIR}")


# AZURE FUNCTION ENTRY POINT

# This function can be triggered via HTTP or Timer Trigger
def main(mytimer=None):
    """
    TimerTrigger example: runs every 5 minutes in Azure Functions
    """
    print(f"Timer trigger fired at {datetime.now()}")
    run_pipeline()


# LOCAL TEST

if __name__ == "__main__":
    main()




