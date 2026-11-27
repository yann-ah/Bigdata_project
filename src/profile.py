import pandas as pd
from common import load
raw, st = load()
df = raw.merge(st, on="station_id")
df["bikes"] = df.mechanical.fillna(0) + df.ebike.fillna(0)
df["ts"] = pd.to_datetime(df.ts, utc=True).dt.tz_convert("Europe/Paris")
df["hour"] = df.ts.dt.hour
df["weekend"] = df.ts.dt.dayofweek >= 5
df = df[df.capacity > 0]
df["fill"] = df.bikes / df.capacity
print(df.groupby(["weekend", "hour", "zone"]).fill.mean().unstack("zone").round(2).to_string())
print("\nTop 10 stations souvent vides (<= 1 velo) :")
print(df.assign(vide=df.bikes <= 1).groupby(["name", "zone"]).vide.mean().sort_values(ascending=False).head(10).round(2))
