"""
This file just reads a text file.
"""

lines = []

with open("read.txt", "r") as file:
    for line in file:
        if "•" in line:

            if line.strip() not in lines:
                lines.append(line.strip())



for l in lines:
    print(l)