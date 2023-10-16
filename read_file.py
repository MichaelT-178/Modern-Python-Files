"""
This file just reads a text file.
"""

import re

pattern = r'"([^"]*)"'

with open("read.txt", "r") as file:
    for line in file:
        matches = re.findall(pattern, line)
        for match in matches:
            print(match)
