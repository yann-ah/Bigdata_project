import os, io, json, boto3, pandas as pd

def load():
    """Charge tous les relevés bruts depuis S3 + la liste des stations."""
    s3 = boto3.client("s3"); b = os.environ["BUCKET"]
    st = pd.DataFrame(json.loads(s3.get_object(Bucket=b, Key="velib_project/raw/stations_info.json")["Body"].read()))
    st = st[["station_id", "name", "capacity", "zone", "center", "lat", "lon"]]
    st["station_id"] = st["station_id"].astype(str)
    frames = []
    for p in s3.get_paginator("list_objects_v2").paginate(Bucket=b, Prefix="velib_project/raw/date="):
        for o in p.get("Contents", []):
            body = s3.get_object(Bucket=b, Key=o["Key"])["Body"].read()
            df = pd.read_csv(io.BytesIO(body), dtype={"station_id": str})
            df["file"] = o["Key"].split("raw/")[1]
            frames.append(df)
    return pd.concat(frames, ignore_index=True), st
