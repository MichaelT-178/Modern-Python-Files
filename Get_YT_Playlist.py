"""
Gets the title and link for every video in a 
YouTube playlist
"""

from pytube import Playlist, YouTube

playlist_url = 'https://youtube.com/playlist?list=PL-TO19HLnaQM-VxPfkQg1jZQSh2RBT9qr&si=ks-mLPfxXhGA8Cz4'

playlist = Playlist(playlist_url)

video_links = []
video_titles = []

for video in playlist.video_urls:
    video = YouTube(video)
    video_links.append(video.watch_url)
    video_titles.append(video.title)

for link, title in zip(video_links, video_titles):
    print(f"Title: {title}")
    print(f"Link: {link}")
    print()

