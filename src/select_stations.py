import json, os, math, requests
BASE = "https://velib-metropole-opendata.smovengo.cloud/opendata/Velib_Metropole"
PER_CENTER = 10
ZONES = {
  "bureaux":     [("Saint-Lazare", 48.8763, 2.3253), ("BnF", 48.8344, 2.3702), ("Opera", 48.8719, 2.3317)],
  "residentiel": [("Gambetta", 48.8647, 2.3985), ("Convention", 48.8369, 2.2965), ("Jules Joffrin", 48.8923, 2.3445)],
  "gare":        [("Gare de Lyon", 48.8443, 2.3744), ("Montparnasse", 48.8420, 2.3219), ("Gare du Nord", 48.8809, 2.3553)],
}
def dist(lat1, lon1, lat2, lon2):
    p = math.pi / 180
    a = math.sin((lat2-lat1)*p/2)**2 + math.cos(lat1*p)*math.cos(lat2*p)*math.sin((lon2-lon1)*p/2)**2
    return 12742000 * math.asin(math.sqrt(a))

info = requests.get(f"{BASE}/station_information.json", timeout=20).json()["data"]["stations"]
chosen = {}
for zone, centers in ZONES.items():
    for cname, clat, clon in centers:
        near = sorted(info, key=lambda s: dist(clat, clon, s["lat"], s["lon"]))
        n = 0
        for s in near:
            if s["station_id"] in chosen:
                continue
            chosen[s["station_id"]] = {**s, "zone": zone, "center": cname,
                                       "dist_m": round(dist(clat, clon, s["lat"], s["lon"]))}
            n += 1
            if n == PER_CENTER:
                break
sel = list(chosen.values())
print(len(sel), "stations,", {z: sum(s["zone"] == z for s in sel) for z in ZONES})
for c in sorted({(s["zone"], s["center"]) for s in sel}):
    print(c, max(s["dist_m"] for s in sel if (s["zone"], s["center"]) == c))
body = json.dumps(sel)
if os.environ.get("LOCAL"):
    os.makedirs("data/raw", exist_ok=True)
    open("data/raw/stations_info.json", "w").write(body)
    print("ecrit en local : data/raw/stations_info.json")
else:
    import boto3
    boto3.client("s3").put_object(Bucket=os.environ["BUCKET"], Key="velib_project/raw/stations_info.json", Body=body.encode())
    print("ecrit sur S3")
