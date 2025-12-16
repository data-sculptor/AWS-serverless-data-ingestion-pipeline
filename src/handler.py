import urllib3
import gzip
from datetime import datetime
from zoneinfo import ZoneInfo
import time
import boto3

http = urllib3.PoolManager()
s3 = boto3.client("s3")

# Parameters
data_type = "fchg"
EVA = "8000237"


bucket_name = "db-api-responses" 


url = "https://apis.deutschebahn.com/db-api-marketplace/apis/timetables/v1/" + data_type + "/" + EVA
headers = {
    "DB-Client-Id": clientId,
    "DB-Api-Key": clientSecret,
    "accept": "application/xml"
}

BERLIN = ZoneInfo("Europe/Berlin")

def lambda_handler(event, context):
    # Call DB API
    resp = http.request("GET", url, headers=headers)

    if resp.status != 200:
        raise Exception(f"DB API error HTTP {resp.status}: {resp.data[:200]!r}")

    data = resp.data  # bytes (XML)

    # gzip compress raw XML bytes
    compressed_file = gzip.compress(data)

    # Berlin timestamp for filename
    ts = datetime.now(BERLIN).strftime("%Y%m%dT%H%M%S%z")  # e.g. 20251216T143012+0100
    year = ts[:4]  # e.g. 2024
    month = ts[4:6]  # e.g. 12
    day = ts[6:8]  # e.g. 16
    hour = ts[9:11]  # e.g. 14

    prefix = f"{EVA}/{data_type}/" + year + "/" + month + "/" + day + "/" + hour + "/"
    key = f"{prefix}{ts}.xml.gz"

    # Upload to S3
    s3.put_object(
        Bucket=bucket_name,
        Key=key,
        Body=compressed_file,
        ContentType="application/gzip"
    )



    return {"ok": True, "keys": [key]}
