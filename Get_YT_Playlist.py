"""
Gets the title and link for every video in a 
YouTube playlist
"""

import json
from pytube import Playlist, YouTube
from termcolor import colored
import os; os.system('clear')

playlist_url = 'https://youtube.com/playlist?list=PL-TO19HLnaQM-VxPfkQg1jZQSh2RBT9qr&si=ks-mLPfxXhGA8Cz4'

class Video:
    def __init__(self, title, link, length):
        self.title = title
        self.link = link 
        self.length = length

print(colored("This will take a second. Be patient.", 'magenta'))

playlist = Playlist(playlist_url)

video_titles = []
video_links = []
video_lengths = []

for video in playlist.video_urls:
    video = YouTube(video)
    video_titles.append(video.title)
    video_links.append(video.watch_url)
    video_lengths.append(video.length)

all_videos = []

if len(video_titles) != len(video_links) != len(video_lengths):
    print(colored("Different number of links, titles, and lengths", 'red'))
    exit(0)

for i in range(len(video_titles)):
    print(f"Title {video_titles[i]}")
    print(f"Links {video_links[i]}")
    print(f"Length {video_lengths[i]}")
    print()

    all_videos.append(Video(video_titles[i], video_links[i], video_lengths[i]))

def has_non_ascii(text):
    return not all(ord(char) < 128 for char in text)

video_list = [] 

for video in all_videos:

    if has_non_ascii(video.title):
        print(f"\nASCII CHAR: {colored(video.title, 'red')}\n")

    video_object = {
        "Title": video.title,
        "Link": video.link,
        "Length": video.length,
        "Start_Time": "",
        "End_Time": ""
    }

    video_list.append(video_object)

final_dict = {
    "comment": "List of video objects",
    "Format": "The time format has to be (00:00:00) or (00:00). Ex: 3:12:11 or 8:07 or 21:32",
    "Videos": video_list
}

write_to_file = input("Do you want to write to json file? : ")

if write_to_file.strip().upper() in ["YES", 'Y']:
    with open('videos.json', 'w') as json_file: 
        json.dump(final_dict, json_file, indent=4)
    print(colored("Successfully written to file", 'green'))
    print()
else: 
    exit()


def seconds_to_time(seconds) -> str:
    """ Converts int seconds to formatted time. """
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

def seconds(time) -> int:
    """ Converts time to seconds """
    t = [int(x) for x in time.split(":")]
    return t[1] + (t[0] * 60) if (len(t) == 2) else t[2] + (t[1] * 60) + (t[0] * 3600)



download_playlist = input("Do you want to download the YouTube playlist? : ")

if download_playlist.strip().upper() in ["YES", 'Y']:

    new_directory = input("Name the directory you want to save the videos to : ")

    os.chdir("..")
   
    os.mkdir(f"{new_directory}")
    print(colored(f"The directory \"{new_directory}\" was successfully created!"))
   
    os.chdir("Modern-Python-Files")

    with open('videos.json', 'r') as file:
        data = json.load(file)

    download_with_time = input("\nReady to download? : ")

    if download_with_time.strip().upper() in ["YES", "Y"]:
        
        os.chdir(f"../{new_directory}")

        for video in data["Videos"]:
            
            if seconds(video.Start_Time) > video.Length or seconds(video.Start_Time) < 0:
                print(f"\n{colored('Invalid Start_Time attribute', 'red')}\n")

            if seconds(video.End_Time) > video.Length or seconds(video.End_Time) < 0:
                print(f"\n{colored('Invalid End_Time attribute', 'red')}\n")

            download_length = seconds_to_time(seconds(video.End_Time) - seconds(video.Start_Time))

            print(f"\nLength of download will be -> {download_length}")
            os.system(f'yt-dlp {video.Title} "{video.Link}" --download-sections "*{video.Start_Time}-{video.End_Time}"')
            print(colored("VIDEO SUCCESSFULLY DOWNLOADED\n", 'green'))

    open_folder = input("\nOpen folder? : ")

    if open_folder.strip().upper() in ["YES", "Y"]:
        os.chdir("..")
        os.system(f"open {new_directory}")

        print(colored("Done", 'green'))
