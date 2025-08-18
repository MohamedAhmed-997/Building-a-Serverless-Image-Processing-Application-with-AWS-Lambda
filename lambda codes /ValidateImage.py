import boto3

def lambda_handler(event, context):
    s3 = boto3.client("s3")
    bucket = event["bucket"]
    key = event["key"]

    # Basic check: accept only jpg/png extension
    if not key.lower().endswith((".jpg", ".jpeg", ".png")):
        return {"bucket": bucket, "key": key, "isValid": False, "error": "Invalid file type"}

    return {"bucket": bucket, "key": key, "isValid": True}
