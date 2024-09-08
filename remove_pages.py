import os

def clean_text_from_file(file_path, start_marker):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
    
    # Find the position of the start marker
    start_index = text.find(start_marker)
    if start_index == -1:
        print(f"'{start_marker}' not found in {file_path}. Skipping file.")
        return
    
    # Extract text starting from the start_marker
    cleaned_text = text[start_index:]
    
    # Overwrite the original file with cleaned text
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(cleaned_text)

def process_folder(base_folder, start_marker):
    for year_folder in os.listdir(base_folder):
        year_folder_path = os.path.join(base_folder, year_folder)
        
        if os.path.isdir(year_folder_path):
            for file_name in os.listdir(year_folder_path):
                if file_name.endswith('.txt'):
                    file_path = os.path.join(year_folder_path, file_name)
                    
                    clean_text_from_file(file_path, start_marker)
                    print(f"Processed and cleaned {file_path}")

# Define the base folder containing year folders
base_folder = 'extracted_texts'  # Replace with your base folder path

# Define the marker to start cleaning
start_marker = "Page 2"

# Process all folders and files
process_folder(base_folder, start_marker)