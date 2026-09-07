"""
CLI Tool to download Instagram videos

Modeled after the existing TikTokDownloader (see TikTok-Video-Downloader-using-Python-and-yt-dlp)

"""

import yt_dlp
import os
import re
import subprocess
import sys
from typing import Optional, Dict, Any
from datetime import datetime
from termcolor import colored as c


class InstagramDownloader:
    def __init__(self, save_path: str = 'tiktok_videos'):
        self.save_path = save_path
        self.create_save_directory()

    def create_save_directory(self) -> None:
        """Create the save directory if it doesn't exist"""
        if not os.path.exists(self.save_path):
            os.makedirs(self.save_path)

    @staticmethod
    def validate_url(url: str) -> bool:
        """ Validate if the provided URL is an Instagram URL """
        instagram_pattern = r'https?://(www\.)?instagram\.com/.*'
        return bool(re.match(instagram_pattern, url))

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
            return f"{custom_name}.mp4"

        return f"instagram_{timestamp}.mp4"

    def download_video(self, video_url: str, custom_name: Optional[str] = None) -> Optional[str]:
        """
        Download Instagram video

        Args:
            video_url (str): URL of the Instagram post/reel
            custom_name (Optional[str]): Custom name for the video file

        Returns:
            Optional[str]: Path to downloaded file if successful, None otherwise
        """
        if not self.validate_url(video_url):
            print("Error: Invalid Instagram URL")
            return None

        filename = self.get_filename(custom_name)
        output_path = os.path.join(self.save_path, filename)

        ydl_opts = {
            'outtmpl': output_path,
            # Force real video+audio, same fix as the JavaFX app —
            # 'best' alone can silently hand back an audio-only stream.
            'format': "bv*[vcodec~='^avc1']+ba[acodec~='^mp4a']/b[ext=mp4]/bv*+ba/b",
            'merge_output_format': 'mp4',
            'noplaylist': True,
            'quiet': False,
            'progress_hooks': [self.progress_hook],
            # 'cookiesfrombrowser': ('chrome',),  # Needed for private accounts / login-walled posts. Intentionally commented out
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:

                # Check formats first
                info = ydl.extract_info(video_url, download=False)

                formats = info.get("formats", [])

                has_video = any(
                    f.get("vcodec") not in (None, "none")
                    for f in formats
                )

                if not has_video:
                    print(
                        c(
                            "\nERROR: No video stream was found for this Instagram post.\n"
                            "This is likely a photo post, private account, or a post\n"
                            "yt-dlp cannot currently extract without login cookies.\n",
                            "red"
                        )
                    )
                    return None

                # Download normally
                ydl.process_info(info)

                print(c(f"Video successfully downloaded: {output_path}", "green"))
                return output_path

        except yt_dlp.utils.DownloadError as e:
            print(c(f"Error downloading video: {str(e)}", "red"))

        except Exception as e:
            print(c(f"An unexpected error occurred: {str(e)}", "red"))

        return None

    def open_save_folder(self) -> None:
        """Open the save folder in the OS file manager (cross-platform, no os.system)."""
        try:
            if sys.platform == "darwin":
                subprocess.run(["open", self.save_path], check=False)
            elif sys.platform.startswith("win"):
                subprocess.run(["explorer", self.save_path], check=False)
            else:
                subprocess.run(["xdg-open", self.save_path], check=False)
        except Exception as e:
            print(c(f"Could not open folder automatically: {str(e)}", "yellow"))


if __name__ == "__main__":
    downloader = InstagramDownloader(save_path='../tiktoks')

    video_url = input(f"{c('Enter Instagram video link', 'magenta')}: ")
    new_file_name = input("\nName the file (w/o extension): ")

    downloader.download_video(video_url, custom_name=new_file_name)

    downloader.open_save_folder()