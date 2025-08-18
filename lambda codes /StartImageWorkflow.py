import json
import boto3

SFN_ARN = "arn:aws:states:<REGION>:<ACCOUNT_ID>:stateMachine:ImagePipeline-Processorr"
sfn = boto3.client("stepfunctions")

def lambda_handler(event, context):
    print("Event received:", json.dumps(event))

    record = event["Records"][0]
    bucket = record["s3"]["bucket"]["name"]
    key = record["s3"]["object"]["key"]

    # Start Step Function
    response = sfn.start_execution(
        stateMachineArn=SFN_ARN,
        input=json.dumps({"bucket": bucket, "key": key})
    )

    print("Step Function started:", response)
    return {"status": "ok"}
