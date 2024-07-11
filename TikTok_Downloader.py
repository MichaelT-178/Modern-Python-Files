"""

This is a command line interface tool to make using
the tiktok-downloader from the link below easier and
more efficient.

https://github.com/n0l3r/tiktok-downloader

tiktok-downloader and tiktoks should be on your main
path for this to work. Ex: /Users/username/tiktoks

"""

import os
import subprocess
from termcolor import colored as c
import requests
#This command worked to install bs4 -> sudo python3 -m pip install bs4

def get_website_link(app_link: str) -> str:
	try:
		response = requests.get(app_link, allow_redirects=True)
		final_url = response.url
		return final_url
	except requests.RequestException as e:
		print(f"An error occurred: {e}")
		return None

def write_to_clipboard(output: str):
	process = subprocess.Popen('pbcopy', env={'LANG': 'en_US.UTF-8'}, stdin=subprocess.PIPE)
	process.communicate(output.encode('utf-8'))

print(c("Remember that you can NOT download slideshows", 'red'))
print(c("The website link will be fetched using the app link and copied to the clipboard.", 'blue'))
print(c("Later when prompted to \"Paste the URL\" paste the website link.", 'cyan'))

link = input("\nEnter TikTok app link: ")

if link.strip():
	website_link = get_website_link(link)[:-1] #remove last " char

	write_to_clipboard(website_link)
	print(c("Website link copied to clipboard", 'green'), end="")
	print(f": {website_link}")
	#webbrowser.open(link.strip())

os.chdir("../tiktok-downloader")
os.system('npm i')
os.system('node cli/index')

#Get most recently downloaded video name
os.chdir("../tiktok-downloader/downloads")
get_file_name = subprocess.check_output("ls -t | head -n 1", shell=True)
name_of_file = get_file_name.decode('utf-8').strip()

# Name is currently just a giant string of integers. Ex: 7215600292283403566.mp4
new_name = input("\nRename the file (w/o extension): ")

new_name = new_name if new_name.strip() else name_of_file[:-4] #get rid of .mp4 extension

# Rename file
os.system(f"mv {name_of_file} \"{new_name}\".mp4")

# Move the file
os.chdir("../..")
os.system(f"mv ./tiktok-downloader/downloads/\"{new_name}\".mp4 ./tiktoks/")

# Open finder to ensure it was downloaded correctly.
os.system(f"open -a Finder ./tiktoks/")
