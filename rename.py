import os
import csv

def rename_files_and_save_to_csv(folder_path, csv_file_name):
    # List to store modified file names
    modified_names = []

    # Iterate through files in the specified folder
    for file in os.listdir(folder_path):
        # Check if the file starts with the specified prefix
        if file.startswith('moved_bmp_files_'):
            # Remove the prefix
            new_name = file[len('moved_bmp_files_'):]
            # Store the new name in the list
            modified_names.append(new_name)

            # Rename the file
            old_file_path = os.path.join(folder_path, file)
            new_file_path = os.path.join(folder_path, new_name)
            os.rename(old_file_path, new_file_path)

    # Save the modified names to a CSV file
    with open(csv_file_name, mode='w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for name in modified_names:
            writer.writerow([name])

# Example usage
folder_path = r'datasets/biovid/imgs'
csv_file_name = r'datasets/biovid/test.csv'
rename_files_and_save_to_csv(folder_path, csv_file_name)
