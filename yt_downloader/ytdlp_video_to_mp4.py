# https://ffmpeg.org/download.html#build-windows [Install or Download ffmpeg]
# pip install yt-dlp

import subprocess
import os

def get_video_files():
    # List all video files in the current directory
    video_files = [f for f in os.listdir() if os.path.isfile(f) and f.endswith(('.mkv', '.webm', '.flv', '.avi', '.mov', '.wmv', '.mp4'))]
    return video_files

def convert_to_mp4(original_file, crf=23, resolution=None):
    # Convert the video to MP4 format with specified quality settings
    mp4_file = os.path.splitext(original_file)[0] + ".mp4"
    
    # Prepare ffmpeg command
    command = ["ffmpeg", "-i", original_file, "-c:v", "libx264", "-crf", str(crf)]
    
    # Add resolution setting if specified
    if resolution:
        command.extend(["-s", resolution])
    
    command.append(mp4_file)
    
    subprocess.run(command)
    print(f"Converted {original_file} to {mp4_file} with CRF {crf} and resolution {resolution if resolution else 'original'}")

    return mp4_file

def print_quality_options():
    print("\nQuality options (CRF values):")
    print("1. Very High Quality (CRF 18)")
    print("2. High Quality (CRF 20)")
    print("3. Medium Quality (CRF 23) [Default]")
    print("4. Low Quality (CRF 28)")
    print("5. Very Low Quality (CRF 32)")

def get_crf_from_selection(selection):
    crf_values = {
        "1": 18,
        "2": 20,
        "3": 23,
        "4": 28,
        "5": 32
    }
    return crf_values.get(selection, 23)  # Default to CRF 23 if selection is invalid

if __name__ == "__main__":
    # List available video files
    video_files = get_video_files()
    print("\nAvailable video files:")
    for i, video_file in enumerate(video_files):
        print(f"{i + 1}. {video_file}")

    # Get the user's selection for the video file
    file_index = int(input("\nEnter the number of the video file you want to convert to MP4: ")) - 1
    selected_file = video_files[file_index]

    # Print quality options
    print_quality_options()
    quality_selection = input("\nEnter the number corresponding to the desired quality: ").strip()
    crf = get_crf_from_selection(quality_selection)
    
    # Get resolution setting from the user
    resolution = input("Enter the resolution (e.g., 1280x720) or leave blank for original: ").strip()
    
    convert_to_mp4(selected_file, crf, resolution if resolution else None)
