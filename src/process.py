"""Traitement des relevés Vélib' (PySpark sur Onyxia).

Étape en cours : vérifier l'accès au bucket S3 et lister les fichiers bruts.
"""
import os

import boto3

BUCKET = os.environ.get("VELIB_BUCKET", "user-y-andorfer-hirsch-ece")
PREFIX_RAW = "velib_project/raw/"


def lister_fichiers_bruts():
    endpoint = os.environ.get("AWS_ENDPOINT_URL") or os.environ.get("AWS_S3_ENDPOINT")
    s3 = boto3.client("s3", endpoint_url=endpoint)
    paginator = s3.get_paginator("list_objects_v2")
    fichiers = []
    for page in paginator.paginate(Bucket=BUCKET, Prefix=PREFIX_RAW):
        for obj in page.get("Contents", []):
            fichiers.append((obj["Key"], obj["Size"]))
    return fichiers


if __name__ == "__main__":
    fichiers = lister_fichiers_bruts()
    print(f"{len(fichiers)} fichiers trouvés sous s3://{BUCKET}/{PREFIX_RAW}")
    for cle, taille in fichiers[:10]:
        print(f"  {cle}  ({taille} octets)")
