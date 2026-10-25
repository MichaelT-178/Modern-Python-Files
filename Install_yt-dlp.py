import os
import subprocess
import webbrowser

"""
This file is to help you download yt-dlp on your machine.
If you have homebrew installed already this will go a lot
faster. Also this program installs pip which can used to 
download other python libraries and programs.
"""

def printColorfulMessage(txt: str, num: int):
    """ 
    31 is red
    32 is green
    34 is blue
    35 is magenta 
    36 is cyan
    """
    print(f"\u001B[{num}m{txt}\u001B[0m")

printColorfulMessage("THIS THING WILL (MIGHT) TAKE A *LONG* TIME TO RUN. I STRONGLY SUGGEST BEING ON WIFI AND NOT A HOTSPOT", 31)
printColorfulMessage("Installing yt-dlp", 32)
subprocess.run("sudo curl -L https://yt-dl.org/downloads/latest/youtube-dl -o /usr/local/bin/youtube-dl", shell=True)
subprocess.run("sudo chmod a+rx /usr/local/bin/youtube-dl", shell=True)

print("\n\n\n\n")

printColorfulMessage("Installing Homebrew", 35)
printColorfulMessage("This will take a WHILE", 31)
subprocess.run('/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)"', shell=True)

print("\n\n\n\n")

printColorfulMessage("Checking homebrew is installed.", 34)
printColorfulMessage("If this just outputs warnings, you're good", 32)
subprocess.run('brew doctor', shell=True)

printColorfulMessage("Installing pip.", 35)
subprocess.run('curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py', shell=True)


printColorfulMessage("Checking that pip is installed. Should return a version", 32)
print("The output: ", end="", flush=True)
subprocess.run("pip --version", shell=True)

print("\n\n\n\n")
printColorfulMessage("Installing yt-dlp.", 31)
subprocess.run("brew install ffmpeg", shell=True)
subprocess.run("brew install yt-dlp", shell=True)
subprocess.run("brew upgrade", shell=True)

print("\n\n\n\n")

printColorfulMessage('Checking yt-dlp installed correctly. Should output /opt/homebrew/bin/yt-dlp', 36)
print("The output: ", end="", flush=True)
subprocess.run("which yt-dlp", shell=True)

print("\n\n\n\n")
printColorfulMessage("Reverting to stable (This might be unnecessary). ", 31)
subprocess.run("pip uninstall yt-dlp", shell=True)
subprocess.run("pip uninstall yt-dlp", shell=True)

print("\n\n\n\n")

printColorfulMessage("Making updates to brew package", 35)

subprocess.run('brew upgrade librist', shell=True)
subprocess.run('brew upgrade mbedtls', shell=True)

print("\n\n\n\n")

printColorfulMessage("Congratulations! yt-dlp should now be installed", 32)

open_repo = input("\nDo you want to open the command-line interface program repo I made for yt-dlp (y/n) ? : ")

if open_repo.strip().upper() in ["YES", "Y"]:
    webbrowser.open("https://github.com/MichaelT-178/Ancient-Python-Files/blob/main/newer_old_files/YT_downloader_helper.py")
    

