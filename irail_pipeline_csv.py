"""
iRail CSV Pipeline
Author: You
Purpose:
- Fetch live departures, connections, and train positions from iRail
- Store all data in CSV files
- Requires only `requests` library
"""

import os
import csv
import datetime
import requests
from pathlib import Path


# CONFIGURATION


IRAIL_BASE_URL = "https://api.irail.be"
HEADERS = {"User-Agent": "iRail CSV Pipeline"}

# Where CSV files will be stored
DATA_DIR = Path(os.getenv("DATA_DIR", "./data"))
DATA_DIR.mkdir(exist_ok=True)

# Stations to track
STATIONS = [
    "Gent-Sint-Pieters",
    "Brussels-Central",
    "Antwerpen-Centraal"
]

# Example routes to track
ROUTES = [
    ("Gent-Sint-Pieters", "Brussels-Central")
]


# CSV HELPERS


def append_csv(file: Path, fieldnames, rows):
    """Append rows to a CSV file, creating header if not exists."""
    file_exists = file.exists()
    with file.open("a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()
        for row in rows:
            writer.writerow(row)

def load_existing_keys(file: Path, key_field: str):
    """Load existing keys to avoid duplicates."""
    if not file.exists():
        return set()
    with file.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return {row[key_field] for row in reader}

# iRail API FUNCTIONS


def fetch_live_departures(station):
    url = f"{IRAIL_BASE_URL}/liveboard/"
    params = {"station": station, "format": "json"}
    response = requests.get(url, headers=HEADERS, params=params, timeout=10)
    response.raise_for_status()
    return response.json()

def fetch_connections(from_station, to_station):
    url = f"{IRAIL_BASE_URL}/connections/"
    params = {"from": from_station, "to": to_station, "format": "json"}
    response = requests.get(url, headers=HEADERS, params=params, timeout=10)
    response.raise_for_status()
    return response.json()

def fetch_vehicle(vehicle_id):
    url = f"{IRAIL_BASE_URL}/vehicle/"
    params = {"id": vehicle_id, "format": "json"}
    response = requests.get(url, headers=HEADERS, params=params, timeout=10)
    response.raise_for_status()
    return response.json()

# PROCESS FUNCTIONS


def process_live_departures(station):
    data = fetch_live_departures(station)

    stations_file = DATA_DIR / "stations.csv"
    trains_file = DATA_DIR / "trains.csv"
    departures_file = DATA_DIR / "departures.csv"

    existing_trains = load_existing_keys(trains_file, "train_id")

    # Add station record
    append_csv(
        stations_file,
        ["station_name", "recorded_at"],
        [{"station_name": station, "recorded_at": datetime.datetime.utcnow().isoformat()}]
    )

    train_rows = []
    departure_rows = []

    for dep in data.get("departures", {}).get("departure", []):
        train_id = dep.get("vehicle")
        if not train_id:
            continue
        train_type = dep.get("type", "UNKNOWN")
        if train_id not in existing_trains:
            train_rows.append({"train_id": train_id, "train_type": train_type})

        scheduled = datetime.datetime.fromtimestamp(int(dep["time"]))
        delay = int(dep.get("delay", 0))
        actual = scheduled + datetime.timedelta(seconds=delay)

        departure_rows.append({
            "station": station,
            "train_id": train_id,
            "destination": dep["destination"]["name"],
            "platform": dep.get("platform"),
            "scheduled_time": scheduled.isoformat(),
            "actual_time": actual.isoformat(),
            "delay_seconds": delay,
            "train_type": train_type,
            "recorded_at": datetime.datetime.utcnow().isoformat()
        })

    if train_rows:
        append_csv(trains_file, ["train_id", "train_type"], train_rows)
    if departure_rows:
        append_csv(
            departures_file,
            ["station","train_id","destination","platform","scheduled_time",
             "actual_time","delay_seconds","train_type","recorded_at"],
            departure_rows
        )

def process_connections(from_station, to_station):
    data = fetch_connections(from_station, to_station)
    connections_file = DATA_DIR / "connections.csv"
    rows = []
    for conn in data.get("connection", []):
        duration = int(conn["duration"]) // 60
        transfers = len(conn.get("vias", {}).get("via", []))
        rows.append({
            "from_station": from_station,
            "to_station": to_station,
            "total_duration_minutes": duration,
            "transfer_count": transfers,
            "recorded_at": datetime.datetime.utcnow().isoformat()
        })
    if rows:
        append_csv(connections_file, ["from_station","to_station","total_duration_minutes","transfer_count","recorded_at"], rows)

def process_vehicle_positions(train_id):
    data = fetch_vehicle(train_id)
    positions_file = DATA_DIR / "train_positions.csv"
    rows = []
    for stop in data.get("stops", {}).get("stop", []):
        info = stop.get("stationinfo", {})
        if "locationX" in info and "locationY" in info:
            rows.append({
                "train_id": train_id,
                "latitude": info["locationY"],
                "longitude": info["locationX"],
                "recorded_at": datetime.datetime.utcnow().isoformat()
            })
    if rows:
        append_csv(positions_file, ["train_id","latitude","longitude","recorded_at"], rows)

# MAIN PIPELINE


def run_pipeline():
    print("Starting iRail CSV pipeline...")
    for station in STATIONS:
        try:
            process_live_departures(station)
        except Exception as e:
            print(f"Error fetching departures for {station}: {e}")

    for route in ROUTES:
        try:
            process_connections(*route)
        except Exception as e:
            print(f"Error fetching connections {route}: {e}")

    print("Pipeline completed successfully.")


# ENTRYPOINT


if __name__ == "__main__":
    run_pipeline()
