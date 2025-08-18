import boto3

DDB_TABLE = "ImagePipeline-Metadata"

def lambda_handler(event, context):
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table(DDB_TABLE)
    key = event["key"]

    item = {
        "imageKey": key,
        "status": "Resized"
    }

    table.put_item(Item=item)
    return {"status": "Metadata stored"}
