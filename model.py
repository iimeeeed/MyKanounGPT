import os
import pytesseract
from pdf2image import convert_from_path

# Set the Tesseract and Poppler paths for macOS
pytesseract.pytesseract.tesseract_cmd = '/opt/homebrew/bin/tesseract'
poppler_path = '/opt/homebrew/Cellar/poppler/24.04.0_1/bin'

base_dir = 'joradp'
output_base_dir = 'extracted_texts'

os.makedirs(output_base_dir, exist_ok=True)

def process_pdf(pdf_path, output_path):
    # Convert PDF to images using Poppler
    images = convert_from_path(pdf_path, poppler_path=poppler_path)
    
    # Open a file to write the extracted text
    with open(output_path, 'w', encoding='utf-8') as file:
        for i, image in enumerate(images):
            text = pytesseract.image_to_string(image, lang='ara')
            file.write(f"Page {i+1}:\n{text}\n")
    print(f"Processed: {pdf_path}")

def is_within_range(filename):
    """Check if the filename is within the range A2005001 to A2015001."""
    try:
        file_number = int(filename[1:8])  # Extract the numeric part of the filename
        return 2005001 <= file_number <= 2015001
    except ValueError:
        return False

for root, dirs, files in os.walk(base_dir):
    for file in files:
        if file.endswith('.pdf'):
            if is_within_range(file):
                print(f"Processing file: {file}")
                # Full path to the current PDF file
                pdf_path = os.path.join(root, file)
                
                relative_path = os.path.relpath(root, base_dir)
                output_dir = os.path.join(output_base_dir, relative_path)
                os.makedirs(output_dir, exist_ok=True)
                
                output_path = os.path.join(output_dir, f'{os.path.splitext(file)[0]}.txt')
                
                process_pdf(pdf_path, output_path)
            else:
                print(f"Skipping file: {file} - Out of range")