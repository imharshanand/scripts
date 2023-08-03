# Name: piexif Version: 1.1.3
# Name: pillow-heif Version: 0.12.0


# Script to convert HEIC (High-Efficiency Image Codec) files to JPEG format while preserving metadata such as timestamps. This script also checks whether the target file already exists, skipping the conversion if necessary.
# Register HEIF opener: Enables PIL (Python Imaging Library) to open HEIC files.
# Get File List: It walks through the specified directory and all subdirectories, looking for files with the .heic extension. It returns a list of all the HEIC files found.
# Convert HEIC to JPEG: This function does the actual conversion. It opens each HEIC file, reads its EXIF data, and saves it as a JPEG file with the same EXIF data (including orientation and timestamp). It also checks if the target file already exists and skips conversion if it does. The converted file names are returned.
# Main Block: The script can be run from the command line, with an optional path argument specifying the directory to be processed. If no path is provided, it uses the current working directory.

# Import necessary modules
import os
import sys
from PIL import Image, ExifTags
from pillow_heif import register_heif_opener
from datetime import datetime
import piexif
import fnmatch

# Register the HEIC opener so the Pillow library can open HEIC files
register_heif_opener()

# Function to get a list of all HEIC files in a directory and its subdirectories
def get_file_list(dir_of_interest):
    file_list = []

    # Walk through the directory structure
    for root, dirs, files in os.walk(dir_of_interest):
        # For each file in the current directory
        for file in files:
            # If the file is a HEIC file
            if fnmatch.fnmatch(file.lower(), '*.heic'):
                # Append the directory and file name to the list
                file_list.append([root.replace('\\', '/').replace('//', '/'), file])

    # Return the list of HEIC files
    return file_list

# Function to convert HEIC files to JPEG
def convert_heic_to_jpeg(dir_of_interest):
    # Get a list of all HEIC files in the directory
    heic_files = get_file_list(dir_of_interest)

    # Initialize a list to keep track of successfully converted files
    success_files = []

    # Print the number of files found
    print(f'Found {len(heic_files)} files to convert in folder {dir_of_interest}')

    # For each HEIC file
    for root, filename in heic_files:

        # Determine the name of the JPEG file
        target_filename = os.path.splitext(filename)[0] + ".jpg"
        target_file = root + "/" + target_filename

        # If the JPEG file already exists, skip the conversion
        if os.path.exists(target_file):
            print(f'File {target_filename} already exists, skip')
            continue

        # Open the HEIC file
        image = Image.open(root + "/" + filename)
        # Get the EXIF data from the image
        image_exif = image.getexif()

        # If the image has EXIF data
        if image_exif:
            # Extract the EXIF tags and values
            exif = {ExifTags.TAGS[k]: v for k, v in image_exif.items() if k in ExifTags.TAGS and type(v) is not bytes}
            # Get the date from the EXIF data
            date = datetime.strptime(exif['DateTime'], '%Y:%m:%d %H:%M:%S')

            # Load the EXIF data using piexif
            exif_dict = piexif.load(image.info["exif"])

            # Update the EXIF data with the date and orientation
            exif_dict["0th"][piexif.ImageIFD.DateTime] = date.strftime("%Y:%m:%d %H:%M:%S")
            exif_dict["0th"][piexif.ImageIFD.Orientation] = 1
            exif_bytes = piexif.dump(exif_dict)

            # Save the image as a JPEG with the updated EXIF data
            image.save(target_file, "jpeg", exif = exif_bytes)
            print(f'Converted image: {filename}')

            # Add the file to the list of successfully converted files
            success_files.append(filename)
        else:
            print(f"Unable to get exif data for {filename}")

    # Return the list of successfully converted files
    return success_files

# Main function
if __name__ == '__main__':
    # Get the current directory
    path = os.path.abspath(os.getcwd())

    # If a directory was provided as an argument, use that instead
    if len(sys.argv) > 1:
        path = sys.argv[1]

    # Convert the HEIC files to JPEG
    converted = convert_heic_to_jpeg(path)
    print(f'\nSuccessfully converted {len(converted)} files')

    # Wait for the user to press enter before closing
    input("Press Enter to continue...")
