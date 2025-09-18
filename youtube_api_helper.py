from datetime import datetime
import isodate
import requests
import json
import re
import pytz


def get_api_key():
    """
    Fetches the YouTube API key from a JSON file.
    """
    with open("credentials/youtube_api_key.json", 'r') as file:
        content = json.load(file)
        return content['api_key']

def extract_video_id(url):
    """
    Extracts the video ID from various YouTube URL formats.
    """
    patterns = [
        r"(?:v=|\/videos\/|embed\/|youtu\.be\/|\/shorts\/|\/live\/)([a-zA-Z0-9_-]{11})"
    ]

    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)

    raise ValueError("Invalid YouTube URL")

def get_video_details(api_key, video_id):
    """
    Fetches video details from the YouTube API.
    """
    url = f"https://www.googleapis.com/youtube/v3/videos?id={video_id}&part=snippet,contentDetails,statistics&key={api_key}"

    response = requests.get(url)

    if response.status_code == 200:
        return response.json()
    
    raise RuntimeError(f"API Error: {response.status_code}, {response.text}")


def get_video_upload_time(url):
    """
    Fetches the exact upload datetime of a YouTube video in EST/EDT.

    Args:
        url (str): The YouTube video URL.

    Returns:
        str: The upload time in EST/EDT, formatted nicely.
    """
    api_key = get_api_key()
    video_id = extract_video_id(url)
    video_data = get_video_details(api_key, video_id)

    published_at = video_data['items'][0]['snippet']['publishedAt']

    utc_time = datetime.fromisoformat(published_at.replace("Z", "+00:00"))

    eastern = pytz.timezone("America/New_York")
    local_time = utc_time.astimezone(eastern)

    return local_time.strftime("%B %d, %Y at %I:%M %p %Z")


class CustomYouTubeAPI:
    def get_video_length(url):
        """
        Fetches the length of a YouTube video in seconds.
        
        Args:
            url (str): The YouTube video URL.
        
        Returns:
            int: The length of the video in seconds.
        """
        api_key = get_api_key()
        video_id = extract_video_id(url)
        video_data = get_video_details(api_key, video_id)

        iso_duration = video_data['items'][0]['contentDetails']['duration']
        duration = isodate.parse_duration(iso_duration)
        
        return int(duration.total_seconds())
