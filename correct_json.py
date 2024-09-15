import os
import json
from ar_corrector.corrector import Corrector
  # Adjust import if needed

def correct_text(text):
    """
    Correct the Arabic text using ar-corrector.
    """
    corrector = Corrector()
    corrected_text = corrector.contextual_correct(text)
    return corrected_text

def apply_ar_corrector(input_folder, output_folder):
    """
    Traverse the JSON folder, correct the text using ar-corrector, and save it back.
    """
    for root, dirs, files in os.walk(input_folder):
        for file in files:
            if file.endswith(".json"):  # Process only JSON files
                year = os.path.basename(root)  # Get the year from the folder name
                doc_number = os.path.splitext(file)[0]  # Get the document number

                input_file_path = os.path.join(root, file)
                output_year_folder = os.path.join(output_folder, year)

                # Load the JSON data
                with open(input_file_path, 'r', encoding='utf-8') as json_file:
                    data = json.load(json_file)

                # Correct the text in each page
                corrected_data = {}
                for page_number, page_text in data.items():
                    corrected_text = correct_text(page_text)
                    corrected_data[page_number] = corrected_text

                # Create output directories if they don't exist
                os.makedirs(output_year_folder, exist_ok=True)

                # Save the corrected data as JSON
                output_file_path = os.path.join(output_year_folder, f'{doc_number}.json')
                with open(output_file_path, 'w', encoding='utf-8') as json_file:
                    json.dump(corrected_data, json_file, ensure_ascii=False, indent=4)

                print(f"Corrected {input_file_path} -> {output_file_path}")

# Example usage
input_folder = "json_data"  # e.g., "json_data"
output_folder = "json_data_corrected"  # e.g., "corrected_json_data"

apply_ar_corrector(input_folder, output_folder)