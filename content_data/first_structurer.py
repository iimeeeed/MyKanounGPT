import os
from bs4 import BeautifulSoup

# Directory containing HTML files
input_directory = 'output_html'
output_directory = 'output_html_first'

# Ensure the output directory exists
os.makedirs(output_directory, exist_ok=True)

def transform_html(file_path, output_path):
    # Read the HTML file
    with open(file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()

    # Parse HTML content
    soup = BeautifulSoup(html_content, 'html.parser')

    # Find all <tr> elements with the specific bgcolor attribute
    target_trs = soup.find_all('tr', {'bgcolor': '#78a7b9'})

    # Iterate over each matching <tr>
    for target_tr in target_trs:
        # Find the next 4 <tr> elements (excluding the current one)
        following_trs = target_tr.find_all_next('tr', limit=5)

        # Only proceed if there are at least 5 <tr>s (including the current one and the 4 after it)
        if len(following_trs) > 1:
            # Create a new <div> with class "Main"
            main_div = soup.new_tag('div', **{'class': 'Main'})
            
            # Move the next 4 <tr> elements inside the <div>
            for tr in following_trs[1:]:
                main_div.append(tr.extract())  # Extract <tr> and add it to the new <div>

            # Insert the new <div> after the current <tr>
            target_tr.insert_after(main_div)

    # Write the modified HTML to a new file
    with open(output_path, 'w', encoding='utf-8') as file:
        file.write(soup.prettify())

# Process each HTML file in the input directory
for filename in os.listdir(input_directory):
    if filename.endswith('.html'):
        file_path = os.path.join(input_directory, filename)
        output_path = os.path.join(output_directory, filename)
        transform_html(file_path, output_path)

print("Transformation complete. Modified files saved to:", output_directory)