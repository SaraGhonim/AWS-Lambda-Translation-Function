import os
import time
import random
import google.generativeai as genai
from interfaces import ITranslator

class GeminiTranslator(ITranslator):
    """Handles translation using the Gemini API."""
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.5-flash')
        self.retries = 3
        self.delay = 5

    def translate(self, file_path: str) -> str | None:
        """Requests translation of a single PDF file's content."""
        target_language = os.environ.get("TARGET_LANGUAGE", "Arabic")
        with open(file_path, "rb") as f:
            file_bytes = f.read()
        
        for attempt in range(self.retries):
            try:
                print(f"Attempt {attempt + 1}/{self.retries} to translate {os.path.basename(file_path)}...")
                response = self.model.generate_content(
                    contents=[
                        {
                            "inline_data": {
                                "mime_type": "application/pdf",
                                "data": file_bytes
                            }
                        },
                        {
                            "text": f"Translate the contents of this PDF into {target_language}. Maintain the original formatting, headings, bullet points, and structure as much as possible. Return only the translation with the page number صفحة, with no additions, explanations, or suggestions"
                        }
                    ]
                )
                print("Translation successful.")
                return response.text
            except Exception as e:
                print(f"Error while translating {file_path}: {e}")
                if attempt < self.retries - 1:
                    wait_time = self.delay + random.uniform(0, 3)
                    print(f"Retrying in {wait_time:.1f} seconds...")
                    time.sleep(wait_time)
                else:
                    print(f"Max retries reached for {file_path}")
                    with open("errors.log", "a", encoding="utf-8") as log:
                        log.write(f"{file_path} failed: {str(e)}\n")
                    return None