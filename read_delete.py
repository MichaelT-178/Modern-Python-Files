import subprocess

def write_to_clipboard(output: str):
    process = subprocess.Popen('pbcopy', env={'LANG': 'en_US.UTF-8'}, stdin=subprocess.PIPE)
    process.communicate(output.encode('utf-8'))


contents = ""

with open('DELETE.txt', 'r') as file:
    for line in file:
        contents += line.strip()



# print(contents)

# write_to_clipboard(contents)

def seconds_to_time(cool):
    return 20

def time_to_seconds(cool):
    return 1

end_time = 2
start_time = 0

download_length = seconds_to_time(time_to_seconds(end_time) - 
                                  time_to_seconds(start_time))

print(download_length)