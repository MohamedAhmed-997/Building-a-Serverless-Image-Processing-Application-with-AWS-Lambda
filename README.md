# Building a Serverless Image Processing Application with AWS Lambda (Manara-project)

This project provides a step-by-step guide to building a **serverless image processing application** on AWS. Users upload images to an Amazon S3 bucket, which triggers an AWS Lambda function to resize or process the image (e.g., watermarking) before saving it to another S3 bucket. Metadata about each image is stored in DynamoDB for tracking and querying. The project also integrates API Gateway for image upload endpoints and Step Functions for orchestrating workflows.

---

## 📚 Table of Contents

* [🧰 Prerequisites](#-prerequisites)
* [🧱 Project Architecture Overview](#-project-architecture-overview)
* [📦 Create S3 Buckets](#-create-s3-buckets)
* [⚡ Create AWS Lambda Functions](#-create-aws-lambda-functions)
* [🔗 Configure S3 Event Triggers](#-configure-s3-event-triggers)
* [📊 Store Metadata in DynamoDB](#-store-metadata-in-dynamodb)
* [🔄 Orchestrate Workflow with AWS Step Functions](#-orchestrate-workflow-with-aws-step-functions)
* [🌐 Expose Upload API with API Gateway](#-expose-upload-api-with-api-gateway)
* [📡 Monitoring with CloudWatch](#-monitoring-with-cloudwatch)
* [🚀 Validate the Setup](#-validate-the-setup)
* [🧪 Testing the Application](#-testing-the-application)
* [🧼 Optional Cleanup](#-optional-cleanup)
* [🧑‍💻 Author](#-author)
* [📜 License](#-license)

---

## 🧰 Prerequisites

* An AWS account (Free Tier eligible).
* Basic knowledge of AWS Lambda, API Gateway, S3, and DynamoDB.
* AWS CLI or Console access.


---

## 🧱 Project Architecture Overview

The serverless architecture includes:

* **Amazon S3 (Source Bucket)**: Stores original uploaded images.
* **Amazon S3 (Destination Bucket)**: Stores processed images (resized, watermarked).
* **AWS Lambda**: Processes images and writes metadata.
* **Amazon DynamoDB**: Stores metadata (filename, size, timestamp, user ID, etc.).
* **Amazon API Gateway**: Provides REST API endpoints for uploading images.
* **AWS Step Functions**: Orchestrates workflow (upload → process → metadata storage).
* **Amazon CloudWatch**: Monitors logs, Lambda metrics, and Step Functions state transitions.

![Architecture Diagram](images/serverless-architecture.png)

---

## 📦 Create S3 Buckets

1. Navigate to **S3 > Create bucket**.
2. Create two buckets:

   * `image-upload-source` → for raw uploads.
   * `image-processed-output` → for resized/processed images.
3. Enable versioning (optional).
4. Configure bucket policies to allow Lambda access.

---

## ⚡ Create AWS Lambda Functions

 **Two main Lambda functions**:

### 1. `ImageProcessorFunction`

* Triggered when a file is uploaded to `image-upload-source`.
* Use a library (Pillow in Python ) to resize the image.
* Saves processed image to `image-processed-output`.

```python
import boto3
from PIL import Image
import io

s3 = boto3.client('s3')

def lambda_handler(event, context):
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']
    
    # Download image
    file_obj = s3.get_object(Bucket=bucket, Key=key)
    img = Image.open(file_obj['Body'])
    
    # Resize image
    img = img.resize((300, 300))
    buffer = io.BytesIO()
    img.save(buffer, 'JPEG')
    buffer.seek(0)
    
    # Upload to destination bucket
    s3.put_object(Bucket="image-processed-output", Key=key, Body=buffer)
    
    return {"status": "processed", "image": key}
```

---

## 🔗 Configure S3 Event Triggers

1. Go to **S3 > image-upload-source > Properties > Event notifications**.
2. Add event trigger for `PUT` (ObjectCreated).
3. Set destination to **ImageProcessorFunction** Lambda.

---

## 📊 Store Metadata in DynamoDB

* Create a table `ImageMetadata` with:

  * **Partition key**: `image_id` (string).
  * **Sort key**: `timestamp` (number).

Example metadata stored:

```json
{
  "image_id": "user123-photo.jpg",
  "original_bucket": "image-upload-source",
  "processed_bucket": "image-processed-output",
  "size": "300x300",
  "uploaded_at": "2025-08-17T12:30:00Z",
  "user": "user123"
}
```

---

## 🔄 Orchestrate Workflow with AWS Step Functions

1. Go to **Step Functions > Create state machine**.
2. Define workflow in **Amazon States Language (ASL)**:

```json
{
  "Comment": "Image Processing Workflow",
  "StartAt": "ResizeImage",
  "States": {
    "ResizeImage": {
      "Type": "Task",
      "Resource": "arn:aws:lambda:region:acct:function:ImageProcessorFunction",
      "Next": "StoreMetadata"
    },
    "StoreMetadata": {
      "Type": "Task",
      "Resource": "arn:aws:lambda:region:acct:function:MetadataWriterFunction",
      "End": true
    }
  }
}
```

---

## 🌐 Expose Upload API with API Gateway

1. Go to **API Gateway > Create API > HTTP API**.
2. Create endpoint: `POST /upload`.
3. Integrate with a Lambda function that uploads the image into `image-upload-source` S3 bucket.
4. Return the public URL of the uploaded image.

---

## 📡 Monitoring with CloudWatch

* **Lambda Logs**: Check processing success/errors.
* **Step Functions**: View workflow execution history.
* **CloudWatch Alarms**: Create alarms for failed executions.

---

## 🚀 Validate the Setup

1. Upload an image using the API Gateway endpoint.
2. Confirm it appears in the **image-upload-source** bucket.
3. Wait for Lambda to process → check **image-processed-output** bucket.
4. Verify metadata is written to the **DynamoDB table**.
5. Check that the **Step Functions execution** succeeded.

---

## 🧪 Testing the Application

* Upload multiple images in parallel.
* Test with large file sizes.
* Verify that DynamoDB stores correct metadata.
* Simulate Lambda failure (e.g., invalid file type) and confirm Step Functions handles error.

---

## 🧼 Optional Cleanup

* Delete S3 buckets (both source and processed).
* Delete Lambda functions.
* Delete DynamoDB table.
* Delete API Gateway API.
* Delete Step Function.

---

## 🧑‍💻 Author

GitHub: [@MohamedAhmed-997](https://github.com/yourusername)

---

## 📜 License

This project is licensed under the MIT License. See the `LICENSE` file for details.


