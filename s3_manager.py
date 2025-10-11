import os
import boto3

class S3Manager:
    """Manages all interactions with Amazon S3."""
    def __init__(self):
        self.s3_client = boto3.client('s3')

    def download_file(self, bucket: str, key: str, local_path: str):
        """Downloads a file from S3."""
        print(f"Downloading {key} from {bucket}...")
        self.s3_client.download_file(bucket, key, local_path)
        print("Download successful.")

    def upload_file(self, local_path: str, bucket: str, key: str):
        """Uploads a file to S3."""
        if not os.path.exists(local_path):
            raise FileNotFoundError(f"File to upload not found at {local_path}")
        
        print(f"Uploading {local_path} to S3: {key}")
        self.s3_client.upload_file(local_path, bucket, key)
        print("Upload successful.")