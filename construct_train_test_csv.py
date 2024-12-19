import os
import csv
import random


def list_bmp_files_to_csv(folder_path, output_train_csv, output_test_csv, train_ratio=0.8):
    # List all BMP files in the specified folder
    bmp_files = [f for f in os.listdir(folder_path) if f.lower().endswith('.bmp')]

    # Shuffle the list of BMP files to ensure randomness
    random.shuffle(bmp_files)

    # Determine the split index based on the defined training ratio
    split_index = int(len(bmp_files) * train_ratio)

    # Split the files into training and testing sets
    train_files = bmp_files[:split_index]
    test_files = bmp_files[split_index:]

    # Save the training BMP file names to the output training CSV file
    with open(output_train_csv, mode='w', newline='') as train_file:
        writer = csv.writer(train_file)
        for bmp_file in train_files:
            writer.writerow([bmp_file])  # Write each file name in a new row

    # Save the testing BMP file names to the output testing CSV file
    with open(output_test_csv, mode='w', newline='') as test_file:
        writer = csv.writer(test_file)
        for bmp_file in test_files:
            writer.writerow([bmp_file])  # Write each file name in a new row


# Example usage
folder_path = r'datasets/biovid/imgs'  # Replace with your BMP folder path
output_train_csv = r'datasets/biovid/train_ids.csv'  # Replace with your desired training output file path
output_test_csv = r'datasets/biovid/test_ids.csv'  # Replace with your desired testing output file path
train_ratio = 1  # Define your training ratio (e.g., 0.8 for 80% training, 20% testing)

list_bmp_files_to_csv(folder_path, output_train_csv, output_test_csv, train_ratio)
