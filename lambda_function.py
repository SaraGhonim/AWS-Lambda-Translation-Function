import json
import os
import tempfile
import boto3
from concurrent.futures import ThreadPoolExecutor, as_completed

from s3_manager import S3Manager
from pdf_handler import PDFHandler
from file_manager import FileManager
from gemini_translator import GeminiTranslator
from interfaces import ITranslator, IFileManager

class TranslationPipeline:
    """Orchestrates the entire translation workflow."""
    def __init__(self, pdf_handler: PDFHandler, translator: ITranslator, file_manager: IFileManager, s3_manager: S3Manager, dest_bucket: str):
        self.pdf_handler = pdf_handler
        self.translator = translator
        self.file_manager = file_manager
        self.s3_manager = s3_manager
        self.dest_bucket = dest_bucket
        self.pages_per_chunk = 10
        self.max_workers = os.cpu_count() or 4  # Number of parallel workers, default to CPU count or 4

    def translate_chunk(self, file_path: str, filename: str, translation_folder: str):
        """Helper method to translate a single PDF chunk and store the result."""
        try:
            translated_text = self.translator.translate(file_path)
            if translated_text:
                txt_filename = filename.replace(".pdf", ".txt")
                self.file_manager.store_translated_text(txt_filename, translated_text, translation_folder)
                return f"Successfully translated {filename}"
            else:
                return f"Translation failed for {filename}"
        except Exception as e:
            return f"Error translating {filename}: {str(e)}"

    def execute_translation_pipeline(self, input_file: str, key: str, temp_dir: str):
        print("Step 1: Dividing PDF into chunks...")
        splitted_pdfs_dir = os.path.join(temp_dir, "Splitted_PDFs")
        self.pdf_handler.divide_pdf_by_pages(input_file, self.pages_per_chunk, splitted_pdfs_dir)

        print("Step 2: Translating chunks in parallel...")
        translation_folder = os.path.join(temp_dir, "Translated_Texts")
        os.makedirs(translation_folder, exist_ok=True)

        # Parallel translation of PDF chunks
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # Submit translation tasks for each chunk
            future_to_file = {
                executor.submit(self.translate_chunk, os.path.join(splitted_pdfs_dir, filename), filename, translation_folder): filename
                for filename in os.listdir(splitted_pdfs_dir)
            }

            # Collect results and handle errors
            for future in as_completed(future_to_file):
                filename = future_to_file[future]
                try:
                    result = future.result()
                    print(result)
                except Exception as e:
                    print(f"Error processing {filename}: {str(e)}")

        print("Step 3: Combining translated texts...")
        merged_output_dir = os.path.join(temp_dir, "Merged_Output")
        output_file_path = self.file_manager.combine_translated_files(translation_folder, merged_output_dir)

        print("Step 4: Uploading result to S3...")
        output_key = f"{os.path.splitext(key)[0]}.txt"
        self.s3_manager.upload_file(output_file_path, self.dest_bucket, output_key)


def lambda_handler(event, context):
    """The entry point for the AWS Lambda function."""
    try:
        source_bucket = event['Records'][0]['s3']['bucket']['name']
        key = event['Records'][0]['s3']['object']['key']
        dest_bucket = os.environ["DEST_BUCKET_NAME"]
        gemini_api_key = os.environ["GEMINI_API_KEY"]

        if os.path.splitext(key)[1].lower() != ".pdf":
            raise ValueError(f"Unsupported file extension for key: {key}")

        with tempfile.TemporaryDirectory() as tmpdirname:
            s3_manager = S3Manager()

            local_input_file = os.path.join(tmpdirname, os.path.basename(key))
            s3_manager.download_file(source_bucket, key, local_input_file)

            pipeline = TranslationPipeline(
                pdf_handler=PDFHandler(),
                translator=GeminiTranslator(api_key=gemini_api_key),
                file_manager=FileManager(),
                s3_manager=s3_manager,
                dest_bucket=dest_bucket
            )
            pipeline.execute_translation_pipeline(local_input_file, key, tmpdirname)

            return {
                'statusCode': 200,
                'body': json.dumps(f"Successfully translated file: {key}")
            }

    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps(f"Error processing file: {str(e)}")
        }