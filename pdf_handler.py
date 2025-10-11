import os
import math
from PyPDF2 import PdfReader, PdfWriter

class PDFHandler:
    """Handles splitting of PDF files."""
    def divide_pdf_by_pages(self, input_path: str, pages_per_chunk: int, output_dir: str):
        os.makedirs(output_dir, exist_ok=True)
        reader = PdfReader(input_path)
        total_pages = len(reader.pages)
        chunks_num = math.ceil(total_pages / pages_per_chunk)

        print(f"Dividing PDF into {chunks_num} parts...")
        for i in range(chunks_num):
            writer = PdfWriter()
            start = i * pages_per_chunk
            end = min(start + pages_per_chunk, total_pages)

            for page_num in range(start, end):
                writer.add_page(reader.pages[page_num])

            file_name = f"pages_{start+1}-{end}.pdf"
            file_path = os.path.join(output_dir, file_name)

            with open(file_path, "wb") as out_file:
                writer.write(out_file)
        print("PDF division complete.")