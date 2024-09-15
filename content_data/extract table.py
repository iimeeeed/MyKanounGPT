import os
import json
import re
from bs4 import BeautifulSoup

def clean_text(text):
    # Replace newlines with spaces and remove excessive spaces
    return re.sub(r'\s+', ' ', text).strip()

def parse_html_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    soup = BeautifulSoup(content, 'html.parser')
    
    # Initialize the structured data
    structured_data = []
    current_decree = None
    
    # Loop over all rows in the table
    for row in soup.find_all('tr'):
        row_text = row.get_text(strip=True)
        row_html = str(row)
        
        # Clean the text to remove excessive spaces and newlines
        clean_row_text = clean_text(row_text)
        
        # Detect new decree (main sections)
        if "تفاصيل" in clean_row_text and 'bgcolor="#78a7b9"' in row_html:
            if current_decree is not None:
                structured_data.append(current_decree)  # Save the previous decree
            current_decree = {"level": 1, "details": []}

        elif 'color="Maroon"' in row_html:
            if current_decree is not None:
                structured_data.append(current_decree)  # Save the previous decree
            current_decree = {"level": 0, "details": [clean_row_text]}

        elif "تفاصيل" in clean_row_text and 'bgcolor="#9ec7d7"' in row_html:
            if current_decree is not None:
                structured_data.append(current_decree)  # Save the previous decree
            current_decree = {"level": 2, "details": []}

        elif "تفاصيل" in clean_row_text and 'bgcolor="#c8e7f3"' in row_html:
            if current_decree is not None:
                structured_data.append(current_decree)  # Save the previous decree
            current_decree = {"level": 3, "details": []}

        else:
            if current_decree is not None:
                current_decree["details"].append(clean_row_text)

    # Append the last decree to the structured data
    if current_decree is not None:
        structured_data.append(current_decree)
    
    return structured_data

def write_to_json(structured_data, output_file):
    with open(output_file, 'w', encoding='utf-8') as json_file:
        json.dump(structured_data, json_file, ensure_ascii=False, indent=4)

def process_files(input_folder, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        if filename.endswith(".html"):
            input_file = os.path.join(input_folder, filename)
            output_file = os.path.join(output_folder, os.path.splitext(filename)[0] + '.json')
            
            # Parse the HTML file and get structured data
            structured_data = parse_html_file(input_file)
            
            # Write the structured data to a JSON file
            write_to_json(structured_data, output_file)
            print(f"Processed {input_file} and saved to {output_file}")

if __name__ == "__main__":
    # Input and output folders
    input_folder = "content_html"
    output_folder = "content_json"
    
    # Process all HTML files in the input folder
    process_files(input_folder, output_folder)