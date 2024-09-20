import json
import os

# Path to the folder containing the restructured JSON files
folder_path = 'content_json_structured'

# List to hold all restructured JSON objects
combined_json = []

# Iterate over each file in the folder
for filename in os.listdir(folder_path):
    if filename.endswith('.json'):  # Ensure only JSON files are processed
        file_path = os.path.join(folder_path, filename)
        
        # Open and read the JSON file
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            # Ensure data is a list and extend the combined_json list with it
            if isinstance(data, list):
                combined_json.extend(data)
            else:
                combined_json.append(data)

# Save the combined list into a single JSON file
with open('combined_restructured_data.json', 'w', encoding='utf-8') as output_file:
    json.dump(combined_json, output_file, ensure_ascii=False, indent=4)

print("All JSON files have been combined into 'combined_restructured_data.json'")