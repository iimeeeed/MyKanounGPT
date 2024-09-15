import os
import re
import json

def parse_text_by_pages(text):
    """
    Parse the text and split it by pages using the 'Page X:' format.
    """
    page_pattern = r'Page (\d+):'
    current_page = None
    current_text = []
    pages = {}

    lines = text.splitlines()
    for line in lines:
        # Match page number
        page_match = re.search(page_pattern, line)
        if page_match:
            if current_page is not None:
                # Save the previous page
                pages[current_page] = "\n".join(current_text).strip()
            # Start a new page
            current_page = page_match.group(1)
            current_text = []
        else:
            # Append text to the current page
            if current_page:
                current_text.append(line)

    # Save the last page
    if current_page:
        pages[current_page] = "\n".join(current_text).strip()
    
    return pages

def convert_text_files_to_json(input_folder, output_folder):
    """
    Traverse the input folder containing year subfolders and convert text files into JSON format.
    Each year folder will contain JSON files, one for each numbered document with the original name.
    """
    for root, dirs, files in os.walk(input_folder):
        for file in files:
            if file.endswith(".txt"):  # Process only text files
                year = os.path.basename(root)  # Get the year from the folder name
                doc_number = os.path.splitext(file)[0]  # Get the document number (e.g., A1995001)

                input_file_path = os.path.join(root, file)
                output_year_folder = os.path.join(output_folder, year)

                # Read the text file
                with open(input_file_path, 'r', encoding='utf-8') as f:
                    text = f.read()

                # Parse the text by pages
                parsed_data = parse_text_by_pages(text)

                # Create output directories if they don't exist
                os.makedirs(output_year_folder, exist_ok=True)

                # Save the parsed data as JSON with the same document number
                output_file_path = os.path.join(output_year_folder, f'{doc_number}.json')
                with open(output_file_path, 'w', encoding='utf-8') as json_file:
                    json.dump(parsed_data, json_file, ensure_ascii=False, indent=4)

                print(f"Processed {input_file_path} -> {output_file_path}")

# Example usage
input_folder = "extracted_texts"  # e.g., "extracted_texts"
output_folder = "json_data"  # e.g., "json_data"

convert_text_files_to_json(input_folder, output_folder)