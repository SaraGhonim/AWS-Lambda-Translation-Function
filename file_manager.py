import os
import re
from natsort import natsorted
from .interfaces import IFileManager

class FileManager(IFileManager):
    """Manages saving and combining translated text files."""
    def store_translated_text(self, file_name: str, text: str, output_folder: str):
        os.makedirs(output_folder, exist_ok=True)
        
        match = re.search(r'pages_(\d+)-(\d+)', file_name)
        if not match:
            raise ValueError("Filename must match format like 'pages_11-19.txt'")
        
        start_page = int(match.group(1))
        
        pattern = r'(?:صفحة|page)\s+(\d+)'
        
        def replace_page_number(match_obj):
            old_number = int(match_obj.group(1))
            new_number = old_number + start_page - 1
            prefix = match_obj.group(0).split()[0]
            return f"{prefix} {new_number}"

        updated_content = re.sub(pattern, replace_page_number, text, flags=re.IGNORECASE)
        updated_content = f"\n\n{updated_content}\n\n"
        
        txt_path = os.path.join(output_folder, file_name)
        with open(txt_path, "w", encoding="utf-8") as f:
            f.write(updated_content)

    def combine_translated_files(self, input_folder: str, output_folder: str) -> str:
        """Combines all translated text files into a single file."""
        os.makedirs(output_folder, exist_ok=True)
        full_text = ""
        files = natsorted([f for f in os.listdir(input_folder)])

        print("Combining translated text files...")
        for filename in files:
            txt_path = os.path.join(input_folder, filename)
            with open(txt_path, "r", encoding="utf-8") as f:
                full_text += f.read()

        output_path = os.path.join(output_folder, "Translated_Document.txt")
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(full_text)
        print("Combining complete.")
        return output_path