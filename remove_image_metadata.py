import sys
import os
from PIL import Image
import piexif

def remove_metadata_from_folder(folder_path):
    # Create an output folder named 'without_metadata' within the given folder
    output_folder = os.path.join(folder_path, 'without_metadata')
    os.makedirs(output_folder, exist_ok=True)
    
    # Iterate through all files in the given folder
    for filename in os.listdir(folder_path):
        # Check if the file is an image by looking at its extension
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif')):
            # Create the full path to the image
            image_path = os.path.join(folder_path, filename)
            
            # Open the image using PIL
            image = Image.open(image_path)
            
            # Check if the image has EXIF data and remove it if present
            if "exif" in image.info:
                # Load the existing EXIF data
                exif_dict = piexif.load(image.info["exif"])
                
                # Clear the EXIF data by setting each section to an empty dictionary
                for ifd in ("0th", "Exif", "GPS", "1st"):
                    exif_dict[ifd] = {}
                
                # Convert the cleared EXIF data back to bytes
                exif_bytes = piexif.dump(exif_dict)
                image.info["exif"] = exif_bytes

            # Create the full path to the output image
            output_path = os.path.join(output_folder, filename)
            
            # Save the new image without metadata (exif=bytes())
            image.save(output_path, exif=bytes())
            
            print(f"Image {filename} saved without metadata at {output_path}")

if __name__ == "__main__":
    # Check if the correct number of command-line arguments are provided
    if len(sys.argv) != 2:
        print("Usage: python remove_metadata.py <folder_path>")
    else:
        # Get the folder path from the command-line argument
        folder_path = sys.argv[1]
        
        # Call the function to remove metadata from all images in the folder
        remove_metadata_from_folder(folder_path)
        
        print("All images processed successfully.")


"""

The code provided is a comprehensive script designed to remove metadata from all image files within a specified folder. Metadata, in this context, refers to additional information embedded within an image file that may include details such as the camera model, GPS location, date of creation, and other technical attributes. The removal of this data ensures privacy and can also reduce the file size. Below, we'll break down the code to explain its components and functionality.

File Name Suggestion:
remove_image_metadata.py

Code Overview:
Importing Libraries: The code begins by importing necessary libraries:

sys: To access command-line arguments.
os: To interact with the operating system, enabling folder navigation.
PIL (Python Imaging Library): To read and manipulate image files.
piexif: To handle the EXIF data within the images.
Defining the Main Function: The remove_metadata_from_folder function is the core of the script, designed to process all images in a given folder.

Creating Output Folder: Within the target folder, a subfolder named 'without_metadata' is created to store the processed images.

Iterating Through Images: The script scans the specified folder, identifying image files by their extensions (e.g., .jpg, .png).

Opening and Processing Images: For each image file:

It is opened using PIL.
If EXIF data is present, it is loaded and then cleared using the piexif library.
The cleared EXIF data is converted back to bytes.
The image, now without metadata, is saved to the 'without_metadata' subfolder.
Command-Line Integration: The code is structured to be run from the command line, accepting the folder path as an argument.

Usage Message: If the script is run without the correct number of arguments, a usage message is displayed.

Execution: If executed with the correct parameters, the script processes all the images in the specified folder, providing a success message upon completion.

Privacy and Utility:
This code serves a valuable function in various scenarios, especially where privacy is a concern. By removing metadata, it ensures that sensitive information embedded within images is not inadvertently shared. This can be crucial for both personal and professional use, such as sharing photographs on social media or using images in public documents.

Supported Formats:
The script supports popular image formats, including JPEG, PNG, TIFF, BMP, and GIF. It could be extended to support other formats if needed.

Extensibility:
The code is modular and well-commented, allowing for easy customization or expansion. Additional functionalities, such as resizing images or converting between formats, could be integrated without significant restructuring.

Conclusion:
The remove_image_metadata.py script is a robust and user-friendly tool for bulk processing of images to remove metadata. Its design emphasizes privacy, ease of use, and adaptability. The use of standard libraries ensures compatibility and reliability, while its command-line interface provides flexibility for integration into various workflows or automation processes. Whether for individual privacy concerns or broader data management needs, this script offers a streamlined solution for handling image metadata.

"""
