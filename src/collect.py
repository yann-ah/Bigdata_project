import os, json, datetime, boto3, requests
BASE = "https://velib-metropole-opendata.smovengo.cloud/opendata/Velib_Metropole"
bucket = os.environ["BUCKET"]
s3 = boto3.client("s3")
ids = {s["station_id"] for s in json.loads(
    s3.get_object(Bucket=bucket, Key="velib_project/raw/stations_info.json")["Body"].read())}
now = datetime.datetime.now(datetime.timezone.utc)
stations = requests.get(f"{BASE}/station_status.json", timeout=20).json()["data"]["stations"]
lines = ["station_id,ts,mechanical,ebike,docks"]
for s in stations:
    if s["station_id"] in ids:
        t = {k: v for d in s.get("num_bikes_available_types", []) for k, v in d.items()}
        lines.append(f'{s["station_id"]},{now:%Y-%m-%dT%H:%M:%SZ},{t.get("mechanical","")},{t.get("ebike","")},{s["num_docks_available"]}')
key = f"velib_project/raw/date={now:%Y-%m-%d}/status_{now:%H%M}.csv"
s3.put_object(Bucket=bucket, Key=key, Body="\n".join(lines).encode())
print("ecrit", key, len(lines) - 1, "stations")
