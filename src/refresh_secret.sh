#!/bin/bash
# Recree le Secret s3-creds avec les cles S3 actuelles. Ne jamais commiter de cles.
eval "$(python - << 'PY'
import boto3
s = boto3.Session(); c = s.get_credentials().get_frozen_credentials()
print(f"AK='{c.access_key}'; SK='{c.secret_key}'; ST='{c.token or ''}'")
print(f"EP='{s.client('s3').meta.endpoint_url}'")
PY
)"
kubectl create secret generic s3-creds \
  --from-literal=AWS_ACCESS_KEY_ID="$AK" \
  --from-literal=AWS_SECRET_ACCESS_KEY="$SK" \
  --from-literal=AWS_SESSION_TOKEN="$ST" \
  --from-literal=AWS_ENDPOINT_URL="$EP" \
  --from-literal=AWS_DEFAULT_REGION="us-east-1" \
  --from-literal=BUCKET="$BUCKET" \
  --dry-run=client -o yaml | kubectl apply -f -
