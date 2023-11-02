"""
If partially downloading a video doesn't work for some reason.
Download full, convert to mp4, then clip using this.

"""
import os
from termcolor import colored as c

# save_dir = "a_songs_folder"
#save_dir = "Youtube_videos"
save_dir = "Other_Youtube"
video_name = "Inky"



# no extension
path = f"../{save_dir}"
video = f"{path}/\"{video_name}\""

start = "00:02:29"
end = "00:02:46"

os.system(f"ffmpeg -i {video}.mp4 -ss {start} -to {end} -c:v copy -c:a copy {video}_new.mp4")

print("\n\n")

green_y = c("Y", 'green')
red_n = c("N", 'red')

ask_remove = input(f"{c('Do you want to permanently remove the original video', 'red')} {c('(Y/N)', 'blue')} : ")

# Remove the video
if ask_remove.strip().upper() in ["YES", "Y"]: 
    os.remove(f"{path}/{video_name}.mp4") #no quotes 

# Rename clip
os.system(f"mv {video}_new.mp4 {video}.mp4")
          