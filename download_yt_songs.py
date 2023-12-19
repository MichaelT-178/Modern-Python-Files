"""
Downloads a playlist of youtube videos as mp3 files
"""
from pytube import Playlist, YouTube
from termcolor import colored as c
import os; os.system('clear')
import subprocess

# Path where you want the downloaded songs to be
download_path = "../neil_songs"

#Playlist with the songs you're going to download
playlist_url = 'https://youtube.com/playlist?list=PL-TO19HLnaQOR1i3dYdBRGm15w5z2IYBq&si=qrhCJ7LXf3Z7lhz_'

# Change into the directory where you want to save the songs
os.chdir(download_path)

# Print current path
print(c('Current path: ', 'blue'), end="")
curr_path = subprocess.run('pwd', shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
print(f'{curr_path.stdout.strip()}')

start = input("\nStart download (Y/N): ")

# If start not yes exit program
if start.lower().strip() not in ['y', 'yes']:
    exit(0)

playlist = Playlist(playlist_url)
video_links = [YouTube(v).watch_url for v in playlist.video_urls]

# Start downloading the links as mp3's
for link in video_links:
    os.system(f'yt-dlp --extract-audio --audio-format mp3 --prefer-ffmpeg "{link}"')
    print("\n\n")
    print(c("Download complete", 'blue'))
    print("\n\n")

#Clear console
os.system("clear")

def get_file_names(path):
    files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
    return files

file_names = get_file_names(download_path)

print(c("Rename the mp3 files. Press return to not change name\n", "blue"))

for file_name in file_names:

    print(f"Current name: {c(file_name, 'cyan')}")
    new_name = input("New name for file (No extension) : ")

    if new_name.strip() != "" and "mp3" in file_name:
        os.system(f'mv "{file_name[:-4]}".mp3 "{new_name}".mp3')
        print(c("Name successfully changed!\n", 'green'))





