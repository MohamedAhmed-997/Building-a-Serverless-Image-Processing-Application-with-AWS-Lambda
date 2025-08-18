import boto3
from PIL import Image
import io

DEST_BUCKET = "bucket-dest-manara"

def lambda_handler(event, context):
    s3 = boto3.client("s3")
    source_bucket = event["bucket"]
    key = event["key"]
    target_size = (800, 600)

    try:
        obj = s3.get_object(Bucket=source_bucket, Key=key)
        img_data = obj["Body"].read()
        image = Image.open(io.BytesIO(img_data))
        resized = image.resize(target_size, Image.LANCZOS)

        buffer = io.BytesIO()
        resized.save(buffer, format=image.format)
        new_key = f"resized/{key}"
        s3.put_object(Bucket=DEST_BUCKET, Key=new_key, Body=buffer.getvalue())

        return {"bucket": DEST_BUCKET, "key": new_key}
    except Exception as e:
        return {"error": str(e)}
