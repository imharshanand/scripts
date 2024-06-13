# https://ffmpeg.org/download.html#build-windows [Install or Download ffmpeg]
# pip install yt-dlp

import subprocess
import os
import re

def check_ffmpeg_installed():
    """
    Check if ffmpeg is installed by attempting to get its version.
    Returns True if ffmpeg is installed, False otherwise.
    """
    try:
        subprocess.run(["ffmpeg", "-version"], capture_output=True, text=True, check=True)
        return True
    except subprocess.CalledProcessError:
        return False
    except FileNotFoundError:
        return False

def get_available_audio_formats(url):
    """
    Get available audio formats for a given YouTube URL using yt-dlp.
    Returns a list of tuples containing format codes and bitrates.
    """
    # Run yt-dlp to list available formats
    result = subprocess.run(
        ["yt-dlp", "-F", url], capture_output=True, text=True
    )
    formats = result.stdout

    audio_formats = []

    # Parse the output to extract audio formats
    for line in formats.split("\n"):
        if "audio only" in line:
            match = re.search(r"^(\d+).*?(\d+)k", line)
            if match:
                format_code = match.group(1)
                bitrate = int(match.group(2))
                audio_formats.append((format_code, bitrate))

    return audio_formats

def get_video_title(url):
    """
    Get the title of the YouTube video using yt-dlp.
    Returns the title as a string.
    """
    # Run yt-dlp to get the video title
    result = subprocess.run(
        ["yt-dlp", "--get-title", url], capture_output=True, text=True
    )
    title = result.stdout.strip()
    return title

def download_audio(url, audio_format):
    """
    Download the audio from a YouTube video in the specified format.
    The audio is saved as temp_audio.webm.
    Returns the name of the downloaded audio file.
    """
    # Run yt-dlp to download the audio
    subprocess.run(
        ["yt-dlp", f"-f {audio_format}", "-o", "temp_audio.webm", url]
    )
    return "temp_audio.webm"

def convert_to_mp3(audio_file, title):
    """
    Convert the downloaded audio file to MP3 format using ffmpeg.
    The MP3 file is named after the video title.
    Returns the name of the MP3 file.
    """
    # Construct the MP3 filename
    mp3_file = title + ".mp3"
    
    # Check if the audio file exists before converting
    if os.path.exists(audio_file):
        # Run ffmpeg to convert the audio file to MP3
        subprocess.run(
            ["ffmpeg", "-i", audio_file, mp3_file]
        )
        print(f"Converted {audio_file} to {mp3_file}")
        
        # Delete the temporary audio file
        os.remove(audio_file)
        print(f"Deleted temporary file {audio_file}")
    else:
        print(f"Error: {audio_file} not found")
    
    return mp3_file

def print_audio_formats(formats):
    """
    Print the available audio formats.
    """
    print("\nAvailable audio formats:")
    for fmt in formats:
        print(f"Format code: {fmt[0]}, Bitrate: {fmt[1]}k")

if __name__ == "__main__":
    # Check if ffmpeg is installed
    if not check_ffmpeg_installed():
        print("Error: ffmpeg is not installed. Please install ffmpeg and try again.")
        exit(1)

    # Get the YouTube URL from the user
    url = input("Enter the YouTube URL: ")
    
    # Get and print the available audio formats
    audio_formats = get_available_audio_formats(url)
    print_audio_formats(audio_formats)

    # Get the user's selection for the audio format
    selected_audio_format = input("\nEnter the format code for the audio format you want to download: ").strip()

    # Get the video title for naming the MP3 file
    title = get_video_title(url)
    
    # Download the audio in the selected format
    audio_file = download_audio(url, selected_audio_format)
    
    # Convert the downloaded audio to MP3 and delete the temporary file
    convert_to_mp3(audio_file, title)
