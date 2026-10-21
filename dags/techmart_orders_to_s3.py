import json
import sys
import uuid
from datetime import datetime, timezone

import boto3
from airflow.sdk import dag, task


PROJECT_ROOT = "/opt/airflow"

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from ingestion.fetch_orders import fetch_orders


S3_BUCKET = "tech-data-project"
MAX_RECORDS = 1000


@dag(
    dag_id="techmart_orders_to_s3",
    start_date=datetime(2026, 10, 1),
    schedule=None,
    catchup=False,
    tags=["techmart", "ingestion", "aws"],
)
def techmart_orders_to_s3():

    @task
    def extract_and_upload_orders():

        data = fetch_orders()

        orders = data["carts"]

        if not isinstance(orders, list):
            raise ValueError("The carts field must be a list.")

        record_count = len(orders)

        if record_count > MAX_RECORDS:
            raise ValueError(
                f"Record limit exceeded: {record_count}"
            )

   
        now = datetime.now(timezone.utc)
        timestamp = now.strftime("%Y%m%dT%H%M%SZ")
        extract_date = now.strftime("%Y-%m-%d")
        run_token = uuid.uuid4().hex[:8]

        s3_key = (
            f"raw/orders/extract_date={extract_date}/"
            f"orders_{timestamp}_{run_token}.json"
        )


        payload = json.dumps(
            data,
            ensure_ascii=False,
            indent=2,
        ).encode("utf-8")

        session = boto3.Session(profile_name="techmart")
        s3 = session.client("s3")

        # 6. Upload the file to S3.
        s3.put_object(
            Bucket=S3_BUCKET,
            Key=s3_key,
            Body=payload,
            ContentType="application/json",
        )

        result = s3.head_object(
            Bucket=S3_BUCKET,
            Key=s3_key,
        )

        uploaded_size = result["ContentLength"]

        if uploaded_size != len(payload):
            raise ValueError(
                "Uploaded object size does not match the payload size."
            )

        print(f"Orders extracted: {record_count}")
        print(f"S3 bucket: {S3_BUCKET}")
        print(f"S3 key: {s3_key}")
        print(f"Verified object size: {uploaded_size} bytes")

        
        return {
            "record_count": record_count,
            "s3_bucket": S3_BUCKET,
            "s3_key": s3_key,
            "size_bytes": uploaded_size,
        }

    extract_and_upload_orders()


techmart_orders_to_s3()
