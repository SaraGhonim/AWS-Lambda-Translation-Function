# AWS Lambda Translation Function

This project is a serverless AWS Lambda function that automatically translates PDF files into Arabic using the Google Generative AI (Gemini 2.5 Flash) API. It processes PDFs uploaded to an S3 bucket, translates them while preserving formatting, headings, and page numbers, and stores the translated text in a destination S3 bucket. The solution leverages parallel processing for efficiency and is designed for scalability in a serverless environment.

## 🚀 Features

- **Serverless Automation**: Triggered by PDF uploads to an S3 bucket.
- **High-Quality Translation**: Uses the Gemini 2.5 Flash model to translate PDFs into Arabic, maintaining original structure.
- **Parallel Processing**: Translates PDF chunks concurrently to optimize performance.
- **S3 Integration**: Reads from a source bucket and writes to a destination bucket.
- **Error Handling**: Includes retries for API failures and logging for debugging.

## 🏛 Architecture

The workflow is as follows:
1. A PDF is uploaded to the source S3 bucket, triggering the Lambda function.
2. The Lambda function downloads the PDF and splits it into chunks (10 pages each).
3. Chunks are translated in parallel using the Gemini API.
4. Translated texts are combined into a single file.
5. The final translated text is uploaded to the destination S3 bucket.

```plaintext
[S3 Source Bucket] → [AWS Lambda] → [Gemini API] → [S3 Destination Bucket]


## 📦 Prerequisites

Before using this project, make sure the following resources are created:

### 1. Google Gemini API

- Sign up for [Google Vertex AI](https://cloud.google.com/vertex-ai).
- Enable the Gemini API.
- Generate and securely store your API Key.

### 2. AWS S3 Buckets

Create **two S3 buckets** :

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


## 🛠 Setup Instructions

### 1. Create the Lambda Function

- In the AWS Lambda Console, create a new function with Python 3.10+ as the runtime in the same region as the S3 buckets.
- Attach the role created above to the lambda function.
- Upload the provided code.

### 2. Add the function trigger

- Set the trigger of the lambda function to be the S3 Source pucket. 
- Set the event type to All object create events. 
- Set the suffix: *.pdf , to filter for pdf files.

### 3. Add the Lambda Layer

- Upload the provided layer.zip file as a Lambda layer.
- Attach the layer to the function under Layers in the Lambda Console.

### 4. Configure Environment Variables

- Add Environment variables:
GEMINI_API_KEY = <your-gemini-api-key>
DEST_BUCKET_NAME = <your-destination-bucket>

### 5. Configure Lambda Settings

- Memory: Set to at least 512 MB (adjust based on PDF size).
- Timeout: Set to at least 3 minutes (adjust for larger PDFs).

### 6. Deploy the Function

- Deploy the function and test it by uploading a PDF to the source bucket.
