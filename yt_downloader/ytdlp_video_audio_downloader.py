# https://ffmpeg.org/download.html#build-windows [Install or Download ffmpeg]
# pip install yt-dlp


import subprocess
import re

def get_available_formats(url):
    # Get available formats using yt-dlp
    result = subprocess.run(
        ["yt-dlp", "-F", url], capture_output=True, text=True
    )
    formats = result.stdout

    video_formats = []
    audio_formats = []

    for line in formats.split("\n"):
        # Parse video formats
        if "video only" in line:
            match = re.search(r"^(\d+).*?(\d+x\d+).*?(\d+)k", line)
            if match:
                format_code = match.group(1)
                resolution = match.group(2)
                bitrate = int(match.group(3))
                video_formats.append((format_code, resolution, bitrate))
        # Parse audio formats
        elif "audio only" in line:
            match = re.search(r"^(\d+).*?(\d+)k", line)
            if match:
                format_code = match.group(1)
                bitrate = int(match.group(2))
                audio_formats.append((format_code, bitrate))

    return video_formats, audio_formats

def download_selected_formats(url, video_format, audio_format):
    # Get the title of the video to use as file name
    result = subprocess.run(
        ["yt-dlp", "--get-title", url], capture_output=True, text=True
    )
    title = result.stdout.strip()
    # Download the selected formats
    subprocess.run(
        ["yt-dlp", f"-f {video_format}+{audio_format}", "-o", f"{title}.%(ext)s", url]
    )
    return f"{title}.%(ext)s"

def print_formats(formats, format_type):
    # Print the available formats
    print(f"\nAvailable {format_type} formats:")
    for fmt in formats:
        if format_type == "video":
            print(f"Format code: {fmt[0]}, Resolution: {fmt[1]}, Bitrate: {fmt[2]}k")
        else:
            print(f"Format code: {fmt[0]}, Bitrate: {fmt[1]}k")

if __name__ == "__main__":
    url = input("Enter the YouTube URL: ")
    video_formats, audio_formats = get_available_formats(url)

    print_formats(video_formats, "video")
    print_formats(audio_formats, "audio")

    selected_video_format = input("\nEnter the format code for the video format you want to download: ").strip()
    selected_audio_format = input("Enter the format code for the audio format you want to download: ").strip()

    download_selected_formats(url, selected_video_format, selected_audio_format)
