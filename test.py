from youtube_api_helper import get_video_upload_time

url_list = [
    'https://youtu.be/dQw4w9WgXcQ?si=1f_Y5sNeEL0-O9gj'
]

for url in url_list:
    print(get_video_upload_time(url))