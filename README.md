# aws-lambda-pdf-translator
This project implements a serverless AWS Lambda function that translates PDF files into Arabic using the Google Generative AI (Gemini) API. It maintains the original structure and formatting of the input PDF document.

## 🚀 Features

- Serverless, auto-triggered by S3 upload
- Uses Gemini 2.5 Flash model for translation
- Keeps formatting, structure, and page numbering
- Automatically saves translated output in a separate S3 bucket

## 📦 Prerequisites

Before using this project, make sure the following resources are created:

### 1. Google Gemini API

- Sign up for [Google Vertex AI](https://cloud.google.com/vertex-ai).
- Enable the Gemini API.
- Generate and securely store your API Key.

### 2. AWS S3 Buckets

Create **two S3 buckets**:

- `source-bucket-name`: Where PDFs are uploaded. This bucket **triggers the Lambda**.
- `destination-bucket-name`: Where the translated PDFs will be saved.

### 3. IAM Role for Lambda

Create an IAM role with the following permissions:

#### Policies Required:
- `AmazonS3ReadOnlyAccess` for reading source PDFs
- `AmazonS3FullAccess` for writing to the destination bucket
- `AWSLambdaBasicExecutionRole` for CloudWatch logging
- (Optional) Custom inline policy for tighter security

Attach this role to your Lambda function.

### 📁 Environment Variables

- Set environment variables directly in the AWS Lambda console
- Go to the AWS Lambda Console → Configuration → Environment variables.
- Add:
   GEMINI_API_KEY = your_api_key
,  DEST_BUCKET_NAME = your-bucket



## Notes
- Make sure the Lambda has enough memory (recommend ≥ 512MB) and timeout (≥ 3m)
- Add a layer to the Lambda function. The above layer.zip contains packaged dependencies.
- Deploy Lambda and connect the trigger to the source S3 bucket
- Gemini model used: gemini-2.5-flash
- Only PDF files are supported

