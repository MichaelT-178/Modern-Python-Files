"""
This program is a command line interface program 
for the "yt-dlp" Youtube downloader python library. 
Allows you to choose name of the saved file, choose 
video time intervals, and download the youtube link.
Made on 9/18/2023 
"""

import os; os.system('clear')
import subprocess
from pytube import YouTube
from termcolor import colored as c
import inquirer #pip3 install inquirer

# save_dir = "a_songs_folder"
#save_dir = "Youtube_videos"
save_dir = "Other_Youtube"

CURRENT_DOWNLOAD_PATH = f"../{save_dir}/"

if os.path.exists(CURRENT_DOWNLOAD_PATH):
    os.system(f"open -a Finder '{CURRENT_DOWNLOAD_PATH}'")
    print(f"{c('CURRENT DOWNLOAD PATH', 'magenta')}: {os.path.abspath(CURRENT_DOWNLOAD_PATH)}/")
    print("Finder has been opened to current download path. See updates in real time.")
else:
    print(c(f"\nPath does not exist: \"{CURRENT_DOWNLOAD_PATH}\"", 'red'))
    print("Go and fix path\n")
    exit(0)

def time_to_seconds(time) -> int:
    """ Converts int seconds to formatted time. """
    t = [int(x) for x in time.split(":")]
    return t[1] + (t[0] * 60) if (len(t) == 2) else t[2] + (t[1] * 60) + (t[0] * 3600)

def seconds_to_time(seconds) -> str:
    """ Converts time to seconds """
    if seconds < 60:
        return f"0:{seconds:02}"
    elif seconds < 3600:
        minutes = seconds // 60
        seconds %= 60
        return f"{minutes}:{seconds:02}"
    else:
        hours = seconds // 3600
        seconds %= 3600
        minutes = seconds // 60
        seconds %= 60
        return f"{hours}:{minutes:02}:{seconds:02}"

def get_choice(the_message):
    green_yes = c("Yes", 'green')
    red_no = c('No', 'red')

    print()
    questions = [
        inquirer.List('choice',
                      message=the_message,
                      choices=[green_yes, red_no]
                      ),
    ]

    answers = inquirer.prompt(questions)
    return answers

url = input(f"\nEnter {c('youtube link', 'red')} : ")

video_len = YouTube(url).length

print(f"Video length is {c(seconds_to_time(video_len), 'cyan')}")

message = f"Do you want to download a {c('specific time interval', 'blue')} (y/n) ? "
is_time_interval = get_choice(message)

if "Yes" in is_time_interval['choice'] : #'\x1b[32mYes\x1b[0m' the color made the string weird  
    print("\nThe format has to be (00:00:00) or (00:00). Ex: 3:12:11 or 8:07 or 21:32")

    start_time = input("\nEnter a start time: ").strip()

    while (time_to_seconds(start_time) > video_len):
        print("\nInvalid start time")
        start_time = input("Enter a start time: ").strip()

    end_time = input("Enter an end time: ").strip()

    while (time_to_seconds(start_time) > video_len):
        print("\nInvalid end time")
        end_time = input("Enter an end time: ").strip()

    download_length = seconds_to_time(time_to_seconds(end_time) - time_to_seconds(start_time))

    print(f"\nLength of download will be -> {c(download_length, 'blue')}\n")

    new_name = ""

    rename_message = f"Do you want to rename the file? {c('(y/n)', 'red')} "
    do_rename = get_choice(rename_message)

    if "Yes" in do_rename['choice']: 
        name = input("\nNew name of file (without extension): ")
        new_name = f'-o "{name}.%(ext)s"'
        print(f"File's new name is {c(name, 'blue')}{c('.webm', 'blue')}")

    print()
    download_with_time = get_choice("Ready to download? ")

    if "Yes" in download_with_time['choice']: 

        os.chdir(CURRENT_DOWNLOAD_PATH)

        print()
        os.system(f'yt-dlp {new_name.strip()} "{url.strip()}" --download-sections "*{start_time}-{end_time}"')
        print(c("VIDEO SUCCESSFULLY DOWNLOADED", 'green'))
        
        get_file_name = subprocess.check_output("ls -t | head -n 1", shell=True)
        name_of_file = get_file_name.decode('utf-8').strip()
        name_of_file_wo_extension = name_of_file.rsplit('.', 1)[0]

        print()
        convert_video_message = f"Do you want to convert the video to {c('mp4', 'blue')}? "
        convert_video = get_choice(convert_video_message)

        if "Yes" in convert_video['choice']: 
            os.system(f"ffmpeg -i \"{name_of_file_wo_extension}\".webm \"{name_of_file_wo_extension}\".mp4")
            os.remove(f"{name_of_file_wo_extension}.webm")
            print(c("Successfully deleted the webm file and converted to mp4", 'green'))

        print(c("Done", 'green'))

        exit(0)


new_name = ""

print()
rename_message = f"Do you want to rename the file? {c('(y/n)', 'red')} "
rename_vid = get_choice(rename_message)

if "Yes" in rename_vid['choice']: 
    name = input("\nNew name of file (without extension): ")
    new_name = f'-o "{name.strip()}.%(ext)s"'
    print(f"File's new name is {c(name, 'blue')}{c('.webm', 'blue')}")

print()
download_vid = get_choice("Ready to download? ")

if "Yes" in download_vid['choice']: 
    os.chdir(CURRENT_DOWNLOAD_PATH)

    print()

    #--no-mtime sets the date created to now 
    os.system(f'yt-dlp --no-mtime {new_name} "{url.strip()}"')

    print(c("VIDEO SUCCESSFULLY DOWNLOADED", 'green'))
    
    # Run the shell command and capture its output
    get_file_name = subprocess.check_output("ls -t | head -n 1", shell=True)

    # Convert the byte string to a regular string
    name_of_file = get_file_name.decode('utf-8').strip()
    name_of_file_wo_extension = name_of_file.rsplit('.', 1)[0]
    
    print()
    convert_vid_message = f"Do you want to convert the video to {c('mp4', 'blue')}? "
    convert_vid = get_choice(convert_vid_message)

    if "Yes" in convert_vid['choice']: 
        os.system(f"ffmpeg -i \"{name_of_file_wo_extension}\".webm \"{name_of_file_wo_extension}\".mp4")
        os.remove(f"{name_of_file_wo_extension}.webm")
        print(c("Successfully deleted the webm file and converted to mp4", 'green'))
        
    print(c("Done", 'green'))