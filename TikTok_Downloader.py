"""
CLI Tool to download tiktok videos

Modified version of this
https://github.com/vgvr0/TikTok-Video-Downloader-using-Python-and-yt-dlp

"""

import yt_dlp
import os
import re
from typing import Optional, Dict, Any
from datetime import datetime
from termcolor import colored as c

# Source: https://github.com/vgvr0/TikTok-Video-Downloader-using-Python-and-yt-dlp

class TikTokDownloader:
    def __init__(self, save_path: str = 'tiktok_videos'):
        self.save_path = save_path
        self.create_save_directory()
    
    def create_save_directory(self) -> None:
        """Create the save directory if it doesn't exist"""
        if not os.path.exists(self.save_path):
            os.makedirs(self.save_path)
    
    @staticmethod
    def validate_url(url: str) -> bool:
        """ Validate if the provided URL is a TikTok URL """
        tiktok_pattern = r'https?://((?:vm|vt|www)\.)?tiktok\.com/.*'
        return bool(re.match(tiktok_pattern, url))
    
    @staticmethod
    def progress_hook(d: Dict[str, Any]) -> None:
        """
        Hook to display download progress
        
        Args:
            d (Dict[str, Any]): Progress information dictionary
        """
        if d['status'] == 'downloading':
            progress = d.get('_percent_str', 'N/A')
            speed = d.get('_speed_str', 'N/A')
            eta = d.get('_eta_str', 'N/A')
            print(f"Downloading: {progress} at {speed} ETA: {eta}", end='\r')
        elif d['status'] == 'finished':
            print(c("\nDownload completed, finalizing...", 'green'))
    
    
    def get_filename(self, custom_name: Optional[str] = None) -> str:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if custom_name:
            # return f"{custom_name}_{timestamp}.mp4"
            return f"{custom_name}.mp4"
        
        return f"tiktok_{timestamp}.mp4"
    
    
    def download_video(self, video_url: str, custom_name: Optional[str] = None) -> Optional[str]:
        """
        Download TikTok video
        
        Args:
            video_url (str): URL of the TikTok video
            custom_name (Optional[str]): Custom name for the video file
            
        Returns:
            Optional[str]: Path to downloaded file if successful, None otherwise
        """
        if not self.validate_url(video_url):
            print("Error: Invalid TikTok URL")
            return None

        filename = self.get_filename(custom_name)
        output_path = os.path.join(self.save_path, filename)
        
        ydl_opts = {
            'outtmpl': output_path,
            'format': 'best',
            'noplaylist': True,
            'quiet': False,
            'progress_hooks': [self.progress_hook],
            # 'cookiesfrombrowser': ('chrome',),  # Use Chrome cookies for authentication. Intentionally commented out
            'extractor_args': {'tiktok': {'webpage_download': True}},
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([video_url])
                print(c(f"Video successfully downloaded: {output_path}", 'green'))
                return output_path
                
        except yt_dlp.utils.DownloadError as e:
            print(c(f"Error downloading video: {str(e)}", 'red'))
        except Exception as e:
            print(c(f"An unexpected error occurred: {str(e)}", 'red'))
        
        return None


if __name__ == "__main__":
    downloader = TikTokDownloader(save_path='../tiktoks')
    
    video_url = input("Enter TikTok video link: ")
    new_file_name = input("\nName the file (w/o extension): ")
    
    print(c("\nNOTE: It will say \"Downloading webpage\". That's fine and expected.\n", 'magenta'))
    
    # Basic usage
    # downloader.download_video(video_url)
    
    # With custom filename
    downloader.download_video(video_url, custom_name=new_file_name)

