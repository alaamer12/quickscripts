import os
import moviepy.editor as mp
from concurrent.futures import ThreadPoolExecutor
from tqdm import tqdm
import logging

logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')

def get_video_length(file_path):
    """Get the length of a video file in seconds."""
    try:
        video = mp.VideoFileClip(file_path)
        duration = video.duration
        video.close()
        return duration
    except FileNotFoundError:
        logging.error(f"Error processing {file_path}: File not found")
        return 0
    except Exception as e:
        logging.error(f"Error processing {file_path}: {e}")
        return 0

def calculate_video_length_in_directory(directory):
    """Recursively calculate the total length of all videos in the directory tree."""
    total_length = 0
    video_files = []

    for root, dirs, files in os.walk(directory):
        # Skip the directory if it contains a [DONE] file
        if '[DONE]' in files:
            logging.info(f"Skipping directory: {root} (contains [DONE])")
            continue

        for file in files:
            file_path = os.path.join(root, file)

            # Check if the file is a video (you can modify this based on video extensions)
            if file.lower().endswith(('.mp4', '.mkv', '.avi', '.mov')):
                video_files.append(file_path)

    with ThreadPoolExecutor() as executor:
        video_lengths = list(tqdm(executor.map(get_video_length, video_files), total=len(video_files), unit="file", desc="Calculating video lengths"))

    total_length = sum(video_lengths)
    return total_length

def seconds_to_hhmmss(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = int(seconds % 60)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

# Example usage
directory = r"E:\Learnings\Tours\The Programming Tour\Languages\Python\Videos\DBT"
directory2 = r"E:\Learnings\Tours\The Programming Tour\Languages\Python\Videos\AI"
directory3 = r"E:\Learnings\Tours\The Programming Tour\Languages\Python\Videos\Data Science"
directory4 = r"E:\Learnings\Tours\The Programming Tour\Languages\Python\Videos\Implementations"
directory5 = r"E:\Learnings\Tours\The Programming Tour\Languages\Python\Videos\Networking"
directory6 = r"E:\Learnings\Tours\The Programming Tour\Languages\Python\Videos\Patterns"
# a = calculate_video_length_in_directory(directory)
b = calculate_video_length_in_directory(directory2)
c = calculate_video_length_in_directory(directory3)
# d = calculate_video_length_in_directory(directory4)
# e = calculate_video_length_in_directory(directory5)
g = calculate_video_length_in_directory(directory5)
z = g + b + c
print(seconds_to_hhmmss(z))

