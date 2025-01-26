import isodate
import requests
import json
import re


def get_api_key():
    """
    Fetches the YouTube API key from a JSON file.
    """
    with open("credentials/youtube_api_key.json", 'r') as file:
        content = json.load(file)
        return content['api_key']


def extract_video_id(url):
    """
    Extracts the video ID from a YouTube URL.
    """
    pattern = r"(?:https?://)?(?:www\.)?(?:youtube\.com/watch\?v=|youtu\.be/)([a-zA-Z0-9_-]{11})"

    match = re.match(pattern, url)

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
