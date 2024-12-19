import os
import csv

import os
import csv


def find_missing_csv_files_and_delete(bmp_folder, csv_folder, output_csv):
    # List all BMP files (without extension) in the BMP folder
    bmp_files = {os.path.splitext(f)[0] for f in os.listdir(bmp_folder) if f.lower().endswith('.bmp')}

    # List all CSV files (without extension) in the CSV folder
    csv_files = {os.path.splitext(f)[0] for f in os.listdir(csv_folder) if f.lower().endswith('.csv')}

    # Find BMP files that do not have corresponding CSV files
    missing_csv_files = bmp_files - csv_files  # Set difference

    # Save the missing BMP file names to the output CSV file
    with open(output_csv, mode='w', newline='') as file:
        writer = csv.writer(file)
        for name in missing_csv_files:
            bmp_file_name = name + '.bmp'
            writer.writerow([bmp_file_name])  # Add the '.bmp' extension back

            # Delete the BMP file
            bmp_file_path = os.path.join(bmp_folder, bmp_file_name)
            try:
                os.remove(bmp_file_path)
                print(f"Deleted: {bmp_file_path}")
            except OSError as e:
                print(f"Error deleting file {bmp_file_path}: {e}")


# Example usage
bmp_folder = r'datasets/biovid/imgs'  # Replace with your BMP folder path
csv_folder = r"W:\Nan\OpenFace_2.2.0_win_x64\OpenFace_2.2.0_win_x64\processed"  # Replace with your CSV folder path
output_csv = r'datasets/biovid/missing_files.csv'  # Replace with your desired output file path

find_missing_csv_files_and_delete(bmp_folder, csv_folder, output_csv)
