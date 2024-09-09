import os
import numpy as np
from sentence_transformers import SentenceTransformer

# Load pre-trained model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Paths
input_base_dir = 'extracted_texts' 
output_base_dir = 'vectorized_texts' 

def process_and_vectorize_txt_files(input_dir, output_dir):
    """
    This function reads all .txt files from input_dir, vectorizes the content,
    and saves the embeddings in output_dir maintaining the folder structure.
    """
    for foldername, subfolders, filenames in os.walk(input_dir):
        rel_path = os.path.relpath(foldername, input_base_dir)
        output_folder = os.path.join(output_dir, rel_path)
        os.makedirs(output_folder, exist_ok=True)

        for filename in filenames:
            if filename.endswith('.txt'):
                input_file_path = os.path.join(foldername, filename)
                output_file_path = os.path.join(output_folder, filename.replace('.txt', '.npy'))  # Save as .npy

                with open(input_file_path, 'r', encoding='utf-8') as file:
                    text = file.read()

                embedding = model.encode([text])

                np.save(output_file_path, embedding)

                print(f"Processed and saved: {output_file_path}")

# Call the function
process_and_vectorize_txt_files(input_base_dir, output_base_dir)
