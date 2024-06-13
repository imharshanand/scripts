import os
from PIL import Image
import shutil
import matplotlib.pyplot as plt

# Define the base and modified directories
base_dir = 'dataset'
modified_dir = 'modified'

# Get main folders and subfolders dynamically
main_folders = next(os.walk(base_dir))[1]
subfolders = next(os.walk(os.path.join(base_dir, main_folders[0])))[1]

# Function to create a new directory structure for modified files
def create_modified_structure(modified_dir, main_folders, subfolders):
    """
    Creates a directory structure in the modified directory
    matching the structure of the base directory.
    """
    for main_folder in main_folders:
        for subfolder in subfolders:
            # Create subfolder paths in the modified directory
            new_path = os.path.join(modified_dir, main_folder, subfolder)
            os.makedirs(new_path, exist_ok=True)

# Function to rename files with a consistent name across related folders
def rename_and_copy_files(base_dir, modified_dir, main_folders, subfolders, history_file):
    """
    Renames and copies files from the base directory to the modified directory,
    ensuring that corresponding files across related folders get the same new name.
    """
    with open(history_file, 'w') as file:
        for main_folder in main_folders:
            # Get the list of original and new folder paths
            folder_paths = [os.path.join(base_dir, main_folder, subfolder) for subfolder in subfolders]
            new_folder_paths = [os.path.join(modified_dir, main_folder, subfolder) for subfolder in subfolders]
            
            # List files in the first subfolder (assuming all subfolders have the same filenames)
            files = os.listdir(folder_paths[0])
            files.sort()  # Ensure consistent order

            for i, filename in enumerate(files):
                # Determine new file name
                ext = filename.split('.')[-1]
                new_name = f"IMG_{i+1:04d}.{ext}"
                
                # Rename and copy files in each related subfolder
                for folder_path, new_folder_path in zip(folder_paths, new_folder_paths):
                    old_file = os.path.join(folder_path, filename)
                    new_file = os.path.join(new_folder_path, new_name)
                    shutil.copy(old_file, new_file)
                    log_message = f"Copied and renamed {old_file} to {new_file}"
                    print(log_message)
                    file.write(log_message + '\n')

# Function to display images, segments, and lane markings
def display_images(modified_dir, main_folders, subfolders):
    """
    Displays the first image, segment, and lane marking from each main folder
    and subfolder to verify the renaming and copying process.
    """
    fig, axs = plt.subplots(len(main_folders), len(subfolders), figsize=(12, 12))
    for i, main_folder in enumerate(main_folders):
        for j, subfolder in enumerate(subfolders):
            # Construct path to the first image in the modified directory
            folder_path = os.path.join(modified_dir, main_folder, subfolder)
            files = sorted(os.listdir(folder_path))
            if files:
                img_path = os.path.join(folder_path, files[0])
                image = Image.open(img_path)
                axs[i, j].imshow(image)
                axs[i, j].set_title(f"{main_folder} - {subfolder}")
                axs[i, j].axis('off')
    plt.tight_layout()
    plt.show()

# Create the modified directory structure
create_modified_structure(modified_dir, main_folders, subfolders)

# Run the renaming and copying process with history logging
history_file = 'file_name_history.txt'
rename_and_copy_files(base_dir, modified_dir, main_folders, subfolders, history_file)

# Display the images to verify the renaming and copying
display_images(modified_dir, main_folders, subfolders)

print("Renaming, copying, and display completed.")

"""
The script is designed to rename and copy images, segments, 
and lane marking files from a dataset directory to a 
new directory while maintaining a consistent naming convention 
across related folders. It also logs the renaming actions to a file 
and displays sample images to verify the process.
"""
