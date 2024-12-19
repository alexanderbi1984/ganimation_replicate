import os
import shutil

def move_bmp_files(input_folder):
    # Create a directory for moved BMP files
    moved_folder = os.path.join(input_folder, 'moved_bmp_files')
    os.makedirs(moved_folder, exist_ok=True)

    # Walk through the directory
    for root, dirs, files in os.walk(input_folder):
        for file in files:
            if file.lower().endswith('.bmp'):
                # Construct the full file path
                file_path = os.path.join(root, file)
                # Get the subfolder name and remove "_aligned"
                subfolder_name = os.path.basename(root).replace('_aligned', '')
                # Create the new file name with the modified subfolder name as prefix
                new_file_name = f"{subfolder_name}_{file}"
                # Construct the new file path
                new_file_path = os.path.join(moved_folder, new_file_name)
                # Move the BMP file
                shutil.move(file_path, new_file_path)




# Example usage
input_folder = 'datasets/frame'
move_bmp_files(input_folder)

