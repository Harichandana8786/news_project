import json
import boto3

from datetime import datetime

from modules.config import S3_BUCKET_NAME

# =====================================
# S3 CLIENT
# =====================================

s3 = boto3.client("s3")


def save_to_s3(news_data):

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    file_name = f"news_raw/news_{timestamp}.json"

    json_data = json.dumps(news_data)

    s3.put_object(
        Bucket=S3_BUCKET_NAME,
        Key=file_name,
        Body=json_data,
        ContentType="application/json"
    )

    print(f"Uploaded to S3: {file_name}")