"""
This program is a command line interface program 
for the "yt-dlp" Youtube downloader python library. 
Allows you to choose name of the saved file, choose 
video time intervals, and download the youtube link.
Made on 9/18/2023 
"""

import os; os.system('clear')

try:
    from pytube import YouTube
except ModuleNotFoundError:
    os.system("pip3 install pytube")
    from pytube import YouTube

try:
    from termcolor import colored as c
except ModuleNotFoundError:
    os.system("pip3 install termcolor")
    from termcolor import colored as c

import webbrowser #Just converting to mp4 on website is way faster than function.

CURRENT_DOWNLOAD_PATH = "../../a_songs_folder/"

def time_to_seconds(time) -> int:
    t = [int(x) for x in time.split(":")]
    return t[1] + (t[0] * 60) if (len(t) == 2) else t[2] + (t[1] * 60) + (t[0] * 3600)

def seconds_to_time(seconds) -> str:
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

def has_numbers(inputString):
    return any(char.isdigit() for char in inputString)

print(f"{c('CURRENT DOWNLOAD PATH', 'magenta')}: {os.path.abspath(CURRENT_DOWNLOAD_PATH)}/")

url = input(f"\nEnter {c('youtube link', 'red')} : ")

download_specific_part = input(f"\nDo you want to download a {c('specific time interval', 'blue')}? : ")

while has_numbers(download_specific_part):
    download_specific_part = input("\nDo you want to download a specific time interval? : ")

video_len = YouTube(url).length

print(f"Video length is {seconds_to_time(video_len)}")

if download_specific_part.upper() in ["YES", "Y"]:
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

    print(f"Length of download will be -> {download_length}")

    new_name = ""

    rename = input("Do you want to rename the file? : ")

    if rename.upper() in ["YES", "Y"]:
        name = input("\nName of file (no extension): ")
        new_name = f'-o "{name}.%(ext)s"'

    download_with_time = input("\nReady to download? : ")

    if download_with_time.upper() in ["YES", "Y"]:
        os.chdir(CURRENT_DOWNLOAD_PATH)

        print()
        os.system(f'yt-dlp {new_name.strip()} "{url.strip()}" --download-sections "*{start_time}-{end_time}"')
        print(c("VIDEO SUCCESSFULLY DOWNLOADED", 'green'))

        open_folder = input("\nOpen folder? : ")

        if open_folder.strip().upper() in ["YES", "Y"]:
            os.chdir("..")
            os.system("open a_songs_folder")
        
        open_converter = input("\nOpen website to convert to mp4? : ")
        
        if open_converter.strip().upper() in ["YES", "Y"]:
            webbrowser.open("https://cloudconvert.com/mp4-converter")

        print(c("Done", 'green'))

        exit(0)


new_name = ""

rename = input("Do you want to rename the file? : ")

if rename.strip().upper() in ["YES", "Y"]:
    name = input("\nName of file (no extension): ")
    new_name = f'-o "{name.strip()}.%(ext)s"'

download_ready = input("\nReady to download? : ")

if download_ready.strip().upper() in ["YES", "Y"]:
    os.chdir(CURRENT_DOWNLOAD_PATH)

    print()
    os.system(f'yt-dlp {new_name} "{url.strip()}"')

    print(c("VIDEO SUCCESSFULLY DOWNLOADED", 'green'))
    open_folder = input("\nOpen folder? : ")
    
    if open_folder.strip().upper() in ["YES", "Y"]:
        os.chdir("..")
        os.system("open a_songs_folder")

    open_converter = input("\nOpen website to convert to mp4? : ")
    
    if open_converter.strip().upper() in ["YES", "Y"]:
        webbrowser.open("https://cloudconvert.com/mp4-converter")
        
    print(c("Done", 'green'))
