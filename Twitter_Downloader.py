import os; os.system('clear')
import subprocess
from termcolor import colored as c
import inquirer

CURRENT_DOWNLOAD_PATH = os.path.expanduser("~/TwitterVideos")

if not os.path.exists(CURRENT_DOWNLOAD_PATH):
    print(c(f"\nPath does not exist: \"{CURRENT_DOWNLOAD_PATH}\"", 'red'))
    print(f"Go and create \"{CURRENT_DOWNLOAD_PATH}\" folder\n")
    exit(0)

os.chdir(CURRENT_DOWNLOAD_PATH)
os.system(f"open -a Finder '{CURRENT_DOWNLOAD_PATH}'")
print(f"{c('CURRENT DOWNLOAD PATH', 'magenta')}: {CURRENT_DOWNLOAD_PATH}/")

def get_choice(message):
    print()
    
    return inquirer.prompt([
        inquirer.List('choice', message=message, choices=[c("Yes", 'green'), c("No", 'red')])
    ])['choice']

def time_to_seconds(t):
    parts = list(map(int, t.strip().split(":")))
    return parts[-1] + parts[-2] * 60 + (parts[-3] * 3600 if len(parts) == 3 else 0)

def seconds_to_time(s):
    h, rem = divmod(s, 3600)
    m, s = divmod(rem, 60)
    return f"{h}:{m:02}:{s:02}" if h else f"{m}:{s:02}"

# --------- DOWNLOAD VIDEO FIRST ----------
url = input(f"\nEnter {c('Twitter video URL', 'red')} : ").strip()

rename = get_choice("Do you want to rename the file?")
output_flag = ""

if "Yes" in rename:
    new_name = input("New name of file (without extension): ").strip()
    output_flag = f'-o "{new_name}.%(ext)s"'
    print(f"File will be saved as: {c(new_name + '.webm', 'blue')}")

download_cmd = f'yt-dlp --no-mtime --recode-video mp4 {output_flag} "{url}"'
os.system(download_cmd)
print(c("VIDEO SUCCESSFULLY DOWNLOADED AND CONVERTED TO MP4", 'green'))

# --------- GET DOWNLOADED FILE NAME ----------
file_name = subprocess.check_output("ls -t | head -n 1", shell=True).decode().strip()
file_path = os.path.join(CURRENT_DOWNLOAD_PATH, file_name)

# --------- ASK IF USER WANTS TO TRIM ----------
clip = get_choice("Do you want to trim the video?")

if "Yes" in clip:
    print("\nFormat examples: 0:00 or 1:15 or 0:01:30")

    start = input("Enter start time: ").strip()
    end = input("Enter end time (leave blank to go to end): ").strip()

    new_clip_name = input("\nEnter name for trimmed file (no extension): ").strip()
    clip_path = os.path.join(CURRENT_DOWNLOAD_PATH, f"{new_clip_name}.mp4")
    
    start_sec = time_to_seconds(start)
    end_sec = time_to_seconds(end) if end else None

    duration_flag = f"-t {end_sec - start_sec}" if end_sec else ""
    ffmpeg_cmd = f'ffmpeg -ss {start_sec} -i "{file_path}" {duration_flag} -c copy "{clip_path}"'

    os.system(ffmpeg_cmd)

    print(c("Trimmed file saved successfully!", 'green'))
    open_cmd = f"open '{CURRENT_DOWNLOAD_PATH}'"
    os.system(open_cmd)
    
    delete_og_video = get_choice("Do you want to delete the untrimmed video?")
    
    if "Yes" in delete_og_video:
        os.remove(file_path)
        print(c("Original file deleted.", 'red'))
        
    exit()
    
print(c("Done!", 'green'))
