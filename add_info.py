import os

def add_header_to_file(file_path, year, number):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()

    # Add the "Year: YYYY, Number: NNN" line at the top
    header = f"Year: {year}, Number: {number}\n"
    final_text = header + text  # Prepend the header to the original content

    # Overwrite the original file with the new text (in place)
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(final_text)

def process_folder(base_folder):
    for year_folder in os.listdir(base_folder):
        year_folder_path = os.path.join(base_folder, year_folder)
        
        if os.path.isdir(year_folder_path):
            for file_name in os.listdir(year_folder_path):
                if file_name.endswith('.txt') and file_name.startswith('A'):
                    # Extract year and number from the file name (format: AYYYYNNN.txt)
                    year = file_name[1:5]
                    number = file_name[5:8]
                    
                    file_path = os.path.join(year_folder_path, file_name)
                    
                    add_header_to_file(file_path, year, number)
                    print(f"Processed {file_path} with header 'Year: {year}, Number: {number}'")

# Define the base folder containing year folders
base_folder = 'extracted_texts'  # Replace with your base folder path

# Process all folders and files
process_folder(base_folder)