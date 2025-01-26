import os
from moviepy.video.io.VideoFileClip import VideoFileClip
from termcolor import colored as c

def time_to_seconds(time_str):
    """
    Convert a time string (HH:MM:SS, MM:SS, or SS) to seconds.
    
    Args:
        time_str (str): The time string to convert.
    
    Returns:
        int: The total time in seconds.
    """
    parts = time_str.split(':')
    
    if len(parts) == 3:  # HH:MM:SS
        hours, minutes, seconds = map(int, parts)
        return hours * 3600 + minutes * 60 + seconds
    elif len(parts) == 2:  # MM:SS
        minutes, seconds = map(int, parts)
        return minutes * 60 + seconds
    elif len(parts) == 1:  # SS
        return int(parts[0])
    else:
        raise ValueError(f"Invalid time format: {time_str}")

os.system('clear')

# Have ../ at the beginning and treat it like your 
# in your root directory. We'll also save the file in this path
path_to_original_file = "../a_songs_folder"
print(f"\nTHIS IS THE FILE PATH YOU'RE ON: {c(f'{path_to_original_file}/', 'green')}")

# Get all files in the path_to_original_file
try:
    files = os.listdir(path_to_original_file)
    files = [file for file in files if os.path.isfile(os.path.join(path_to_original_file, file))]
    
    if not files:
        print(c(f"No files found in {path_to_original_file}.", 'red'))
        exit()
        
except FileNotFoundError:
    print(c(f"The directory {path_to_original_file} does not exist.", 'red'))
    exit()

print(f"\nFiles in the {c(path_to_original_file, 'green')} directory:")

for idx, file in enumerate(files, start=1):
    print(f"{idx}. {file}")


while True:
    try:
        selected_number = int(input(c("\nEnter the number of the video you want to clip: ", 'cyan')))

        if 1 <= selected_number <= len(files):
            choice_index = selected_number - 1

            original_file_name = files[choice_index]
            break
        else:
            print(c("Invalid number. Please enter a number from the list.", 'red'))

    except ValueError:
        print(c("Invalid input. Please enter a valid number from the list.", 'red'))


# Full path
original_full_path = path_to_original_file + '/' + original_file_name

print(c(f"This is the file path: {original_full_path}", 'green'))




"""
Main part of script
"""
start_time = input("\nEnter the start time of the clipped video (Ex: 0:10): ")
end_time = input("Enter a end time of the clipped video (Ex: 1:30): ")

start_time_seconds = time_to_seconds(start_time)
end_time_seconds = time_to_seconds(end_time)

new_file_name = input(c("\nName the clipped file (no extension): ", 'magenta'))

output_path = path_to_original_file + '/' + new_file_name + '.mp4'


with VideoFileClip(original_full_path) as video:
    video = video.with_audio(video.audio)

    clipped = video.subclipped(start_time, end_time)

    clipped.write_videofile(
        output_path,
        codec="libx264",
        audio_codec="aac",
        temp_audiofile="temp-audio.m4a",
        remove_temp=True
    )

print(c('\nFile saved successfully!', 'green'))

os.system(f'open {path_to_original_file}')