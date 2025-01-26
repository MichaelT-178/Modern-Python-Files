import os
from termcolor import colored as c

"""
Allows you to clip a video 
NOTE: You need the ffmpeg library installed

brew install ffmpeg
"""

def format_time(time: str) -> str:
    """
    format "H:MM", "MM:SS", or "HH:MM:SS".
    """
    parts = time.split(":")
    
    if len(parts) == 1:
        raise ValueError("Invalid time")
    
    if len(parts) == 2:  # MM:SS 
        hours = 0
        minutes, seconds = parts
    elif len(parts) == 3:  # HH:MM:SS 
        hours, minutes, seconds = parts
    else:
        raise ValueError("Invalid time format.")

    hours = int(hours)
    minutes = int(minutes)
    seconds = int(seconds)
    
    return f"{hours:02}:{minutes:02}:{seconds:02}"

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

# Print a menu of all files in the directory with a number next to it.
print(f"\nFiles in the {c(path_to_original_file, 'green')} directory:")

for idx, file in enumerate(files, start=1):
    print(f"{idx}. {file}")


# Make the user choose a file from the menu
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

start_time = input("\nEnter the start time of the clipped video (Ex: 0:10): ")

end_time = input("Enter the end time for the clipped video (Ex: 1:30): ")

new_file_name = input(c("\nName the clipped file (no extension): ", 'magenta'))


# Format times
start_time = format_time(start_time)
end_time = format_time(end_time)
new_file_path = path_to_original_file + '/' + new_file_name + '.mp4'


# This is the command
# This can cause the start of the video to be black -> ffmpeg -i input.mp4 -ss 00:00:10 -t 00:00:20 -c copy output.mp4
# ffmpeg -i input.mp4 -ss "00:08:16.527" -codec:v libx264 -crf 23 -pix_fmt yuv420p -codec:a aac -f mp4 -movflags faststart output.mp4
# ffmpeg -i input.mp4 -ss "00:04:14.643" -to "00:08:16.527" -codec:v libx264 -crf 23 -pix_fmt yuv420p -codec:a aac -f mp4 -movflags faststart output.mp4
# Solution -> https://www.reddit.com/r/ffmpeg/comments/i4rtab/comment/g0kmjua/?utm_source=share&utm_medium=web3x&utm_name=web3xcss&utm_term=1&utm_content=share_button
os.system(f'ffmpeg -i {original_full_path} -ss {start_time} -to {end_time} -codec:v libx264 -crf 23 -pix_fmt yuv420p -codec:a aac -f mp4 -movflags faststart {new_file_path}')

print(c('\nFile saved successfully!', 'green'))

os.system(f'open {path_to_original_file}')

delete_og_file = input(f"{c('\nDo you want to permanently remove the original video', 'red')} {c('(Y/N)', 'blue')} : ")

if delete_og_file.strip().upper() in ['YES', 'Y']:
    os.remove(original_full_path)
    print(c(f'Original file \"{original_full_path}\" successfully deleted!','green'))

