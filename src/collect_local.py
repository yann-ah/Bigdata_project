import os, json, datetime, requests
BASE = "https://velib-metropole-opendata.smovengo.cloud/opendata/Velib_Metropole"
ids = {s["station_id"] for s in json.load(open("data/raw/stations_info.json"))}

now = datetime.datetime.now(datetime.timezone.utc)
stations = requests.get(f"{BASE}/station_status.json", timeout=20).json()["data"]["stations"]
lines = ["station_id,ts,mechanical,ebike,docks"]
for s in stations:
    if s["station_id"] in ids:
        t = {k: v for d in s.get("num_bikes_available_types", []) for k, v in d.items()}
        lines.append(f'{s["station_id"]},{now:%Y-%m-%dT%H:%M:%SZ},{t.get("mechanical","")},{t.get("ebike","")},{s["num_docks_available"]}')
d = f"data/raw/date={now:%Y-%m-%d}"
os.makedirs(d, exist_ok=True)
path = f"{d}/status_{now:%H%M}.csv"
open(path, "w").write("\n".join(lines))
print(now.isoformat(), path, len(lines) - 1, "stations")
