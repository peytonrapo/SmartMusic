import os
import shutil
import pandas as pd

def move_csv_files(source_folder, destination_folder, threshold_lines=10):
    # Ensure destination folder exists
    os.makedirs(destination_folder, exist_ok=True)

    # List all files in the source folder
    files = os.listdir(source_folder)

    for file_name in files:
        if file_name.endswith(".csv"):
            file_path = os.path.join(source_folder, file_name)

            # Count the number of lines in the CSV file
            with open(file_path, 'r') as file:
                num_lines = sum(1 for line in file)

            # Move the file if the number of lines is less than the threshold
            if num_lines < threshold_lines:
                destination_path = os.path.join(destination_folder, file_name)
                shutil.move(file_path, destination_path)
                print(f"Moved '{file_name}' to '{destination_folder}'")

# Example usage
source_folder = "Kevin"
destination_folder = "garbage"
move_csv_files(source_folder, destination_folder)
