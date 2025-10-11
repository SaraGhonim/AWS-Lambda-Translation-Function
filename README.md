# AWS Lambda Translation Function

This project is a serverless AWS Lambda function that automatically translates PDF files into any language using the Google Generative AI (Gemini 2.5 Flash) API. It processes PDFs uploaded to an S3 bucket, translates them while preserving formatting, headings, and page numbers, and stores the translated text in a destination S3 bucket. The solution leverages parallel processing for efficiency and is designed for scalability in a serverless environment.

## 🚀 Features

- **Serverless Automation**: Triggered by PDF uploads to an S3 bucket.
- **High-Quality Translation**: Uses the Gemini 2.5 Flash model to translate PDFs, maintaining original structure.
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
```

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


## 🛠 Setup Instructions

1. **Create the Lambda Function**:
   - In the AWS Lambda Console, create a new function in the same region as the S3 buckets, with Python 3.10+ as the runtime 
   - Attach the role created above to the lambda function.
   - Upload the provided code 

2. **Set Up the S3 Trigger**
   - Set the trigger of the lambda function to be the S3 Source bucket. 
   - Set the event type to `All object create events`. 
   - Set the suffix: `*.pdf` , to filter for pdf files.

3. **Add the Lambda Layer**:
   - Upload the provided `layer.zip` file as a Lambda layer (contains `google-generativeai`, `natsort` ,`PyPDF2`).
   - Attach the layer to the function under **Layers** in the Lambda Console.

4. **Configure Environment Variables**:
   - Add the **Environment variables** 
     ```plaintext
     GEMINI_API_KEY = <your-gemini-api-key>
     DEST_BUCKET_NAME = <your-destination-bucket>
     TARGET_LANGUAGE = <your_target_language>
     ```

5. **Configure Lambda Settings**:
   - **Memory**: Set to at least 512 MB (adjust based on PDF size).
   - **Timeout**: Set to at least 3 minutes (adjust for larger PDFs).
  
6. **Deploy the Function**:
   - Deploy the function and test it by uploading a PDF to the source bucket.

## 📖 Usage

1. Upload a PDF file to the source S3 bucket (e.g., `my-source-bucket/myfile.pdf`).
2. The Lambda function will:
   - Split the PDF into chunks (10 pages each).
   - Translate each chunk using the Gemini API.
   - Combine translated texts into a single file.
   - Save the result as `myfile.txt` in the destination bucket.
3. Check the destination bucket for the translated text file.

**Example Output**:
- Input: `my-source-bucket/document.pdf`
- Output: `my-destination-bucket/document.txt`

## 🧪 Testing

1. **Local Testing**:
   - Simulate the Lambda event with a sample PDF and mock S3 using `boto3`.
   - Example event:
     ```json
     {
       "Records": [
         {
           "s3": {
             "bucket": { "name": "my-source-bucket" },
             "object": { "key": "test.pdf" }
           }
         }
       ]
     }
     
     ```

2. **AWS Testing**:
   - Upload a small PDF to the source bucket and monitor CloudWatch logs.
   - Verify the translated file appears in the destination bucket.

## 🛑 Troubleshooting

- **Error: "Unsupported file extension"**:
  - Ensure only PDF files are uploaded to the source bucket.
- **Error: Gemini API failures**:
  - Check the API key and ensure billing is enabled in Google Vertex AI.
  - Monitor rate limits; reduce `max_workers` in the code if needed (default: 4).
- **Timeout Issues**:
  - Increase the Lambda timeout (e.g., to 5–10 minutes for large PDFs).
- **Memory Issues**:
  - Increase Lambda memory (e.g., to 1024 MB for large PDFs).
- **Logs**: Check CloudWatch logs for detailed error messages (`errors.log` for translation failures).


## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/YourFeature`).
3. Commit changes (`git commit -m 'Add YourFeature'`).
4. Push to the branch (`git push origin feature/YourFeature`).
5. Open a pull request.

## 📧 Contact

For questions or feedback, open an issue or contact at sara.ghonim2014@gmail.com

