import os
import json

def nest_levels(data):
    # Create a new list to hold the modified data
    modified_data = []
    last_level_1 = None
    last_level_2 = None

    for item in data:
        # If it's a level 1 item, reset and remember it for nesting actions
        if item['level'] == 1:
            # Add the last level 2 (if any) to last level 1 actions and then add the level 1 to the modified data
            if last_level_1 is not None:
                if last_level_2 is not None:
                    last_level_1['actions'].append(last_level_2)
                modified_data.append(last_level_1)
            # Initialize a new level 1 object with an actions list
            last_level_1 = item
            last_level_1['actions'] = []
            last_level_2 = None

        # If it's a level 2 item, remember it for nesting level 3 actions
        elif item['level'] == 2:
            # Add the last level 2 item to the current level 1's actions
            if last_level_2 is not None:
                last_level_1['actions'].append(last_level_2)
            # Initialize the level 2 item with an actions list
            last_level_2 = item
            last_level_2['actions'] = []

        # If it's a level 3 item, nest it inside the last level 2 item
        elif item['level'] == 3:
            if last_level_2 is not None:
                last_level_2['actions'].append(item)
            else:
                print("Warning: level 3 found without preceding level 2")

    # Add the last level 2 and level 1 to the modified_data if they exist
    if last_level_1 is not None:
        if last_level_2 is not None:
            last_level_1['actions'].append(last_level_2)
        modified_data.append(last_level_1)

    return modified_data

def process_json(input_file, output_file):
    # Load the existing JSON data
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Apply the nesting logic
    modified_data = nest_levels(data)

    # Save the modified JSON data to a new file
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(modified_data, f, ensure_ascii=False, indent=4)

    print(f"Processed data saved to {output_file}")

def process_all_json_files(input_folder, output_folder):
    # Ensure the output folder exists
    os.makedirs(output_folder, exist_ok=True)

    # Process each JSON file in the input folder
    for filename in os.listdir(input_folder):
        if filename.endswith(".json"):
            input_file = os.path.join(input_folder, filename)
            output_file = os.path.join(output_folder, filename)

            print(f"Processing file: {input_file}")
            process_json(input_file, output_file)

if __name__ == "__main__":
    # Input folder containing the JSON files and output folder for the processed files
    input_folder = "content_json"  # Replace with your input folder path
    output_folder = "content_json_structured"  # Replace with your output folder path

    # Process all JSON files in the folder
    process_all_json_files(input_folder, output_folder)