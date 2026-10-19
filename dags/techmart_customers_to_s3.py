import json
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path

import boto3
from airflow.sdk import dag, task


# Make the project root available for Python imports.
PROJECT_ROOT = "/opt/airflow"
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from ingestion.fetch_customers import fetch_customers


S3_BUCKET = "tech-data-project"
MAX_RECORDS = 1000


@dag(
    dag_id="techmart_customers_to_s3",
    start_date=datetime(2026, 10, 1),
    schedule=None,
    catchup=False,
    tags=["techmart", "ingestion", "aws"],
)
def techmart_customers_to_s3():

    @task
    def extract_and_upload_customers():
        # Step 1: Fetch the customer response from the API.
        data = fetch_customers()
        customers = data["users"]
        record_count = len(customers)

        # Step 2: Enforce our record limit.
        if record_count > MAX_RECORDS:
            raise ValueError(
                f"Record limit exceeded: {record_count}"
            )

        # Step 3: Create a unique S3 key for this execution.
        now = datetime.now(timezone.utc)
        timestamp = now.strftime("%Y%m%dT%H%M%SZ")
        extract_date = now.strftime("%Y-%m-%d")
        run_token = uuid.uuid4().hex[:8]

        s3_key = (
            f"raw/customers/extract_date={extract_date}/"
            f"customers_{timestamp}_{run_token}.json"
        )

        # Step 4: Convert the API response to JSON bytes.
        payload = json.dumps(
            data,
            ensure_ascii=False,
            indent=2,
        ).encode("utf-8")

        # Step 5: Connect using the existing AWS SSO profile.
        session = boto3.Session(profile_name="techmart")
        s3 = session.client("s3")

        # Step 6: Upload the JSON object to S3.
        s3.put_object(
            Bucket=S3_BUCKET,
            Key=s3_key,
            Body=payload,
            ContentType="application/json",
        )

        # Step 7: Verify the uploaded object's size.
        result = s3.head_object(
            Bucket=S3_BUCKET,
            Key=s3_key,
        )

        uploaded_size = result["ContentLength"]

        if uploaded_size != len(payload):
            raise ValueError(
                "Uploaded object size does not match the payload size."
            )

        print(f"Customers uploaded: {record_count}")
        print(f"S3 bucket: {S3_BUCKET}")
        print(f"S3 key: {s3_key}")
        print(f"Verified object size: {uploaded_size} bytes")

        # Return only small metadata, not the full customer dataset.
        return {
            "record_count": record_count,
            "s3_bucket": S3_BUCKET,
            "s3_key": s3_key,
            "size_bytes": uploaded_size,
        }

    extract_and_upload_customers()


techmart_customers_to_s3()