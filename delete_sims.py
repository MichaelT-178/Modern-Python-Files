"""
Tool to help remove unused XCode simulators that are taking up space.
"""

import os

os.chdir("..")

path = os.path.expanduser("~/Library/Developer/CoreSimulator/Devices")


files = os.listdir(path)

for file in files:
    if file != "device_set.plist":
        confirm = input(f"Do you want to remove the file {file}? : ")
        
        full_path = os.path.join(path, file)
        os.system(f"sudo rm -rf '{full_path}'")