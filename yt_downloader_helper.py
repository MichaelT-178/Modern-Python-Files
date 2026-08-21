"""
Fast YouTube downloader/clipper.

- Uses subprocess.run everywhere (no os.system).
- Can clip a time range without downloading the full video first,
  via yt-dlp's --download-sections (only pulls the needed fragments/byte-range).
- Always outputs a final .mp4 (same fast format selector the flash drive
  script uses: avc1 video + mp4a audio, or a pre-muxed mp4 fallback).
- Lets you name the output file.
"""

import os
import re
import subprocess
import sys

from termcolor import colored as c
from youtube_api_helper import CustomYouTubeAPI, extract_video_id

SAVE_DIR = "a_songs_folder"
DOWNLOAD_PATH = os.path.abspath(f"../{SAVE_DIR}/")


FORMAT = "bv*[vcodec~='^avc1']+ba[acodec~='^mp4a']/b[ext=mp4]"


def ensure_download_path() -> None:
    if not os.path.isdir(DOWNLOAD_PATH):
        print(c(f'\nPath does not exist: "{DOWNLOAD_PATH}"', "red"))
        print(f'Go create "{SAVE_DIR}" folder next to this script.\n')
        sys.exit(1)

    subprocess.run(["open", "-a", "Finder", DOWNLOAD_PATH])
    print(f"{c('DOWNLOAD PATH', 'magenta')}: {DOWNLOAD_PATH}/")


def ask_yes_no(prompt: str) -> bool:
    answer = input(f"{prompt} (y/n): ").strip().lower()
    return answer in ("y", "yes")


def time_to_seconds(value: str) -> int:
    parts = [int(x) for x in value.split(":")]
    
    if len(parts) == 2:
        m, s = parts
        return m * 60 + s
    
    h, m, s = parts
    
    return h * 3600 + m * 60 + s


def seconds_to_time(seconds: int) -> str:
    if seconds < 60:
        return f"0:{seconds:02}"
    
    if seconds < 3600:
        return f"{seconds // 60}:{seconds % 60:02}"
    
    h, rem = divmod(seconds, 3600)
    m, s = divmod(rem, 60)
    
    return f"{h}:{m:02}:{s:02}"


def prompt_clip_range(video_len: int) -> tuple[str, str] | None:
    if not ask_yes_no(f"\nDownload just a {c('specific clip', 'blue')} instead of the whole video?"):
        return None

    print("\nFormat: (00:00:00) or (00:00). Ex: 3:12:11 or 8:07 or 21:32")

    while True:
        start = input("Start time: ").strip()
        end = input("End time: ").strip()
        try:
            start_s, end_s = time_to_seconds(start), time_to_seconds(end)
        except (ValueError, IndexError):
            print(c("Could not parse those times, try again.", "red"))
            continue

        if start_s >= end_s:
            print(c("Start time must be before end time.", "red"))
            continue
        if end_s > video_len:
            print(c("End time is past the end of the video.", "red"))
            continue

        print(f"Clip length -> {c(seconds_to_time(end_s - start_s), 'cyan')}")
        return start, end


def prompt_filename() -> str | None:
    name = input("\nNew file name (no extension): ").strip()
    name = re.sub(r'[\\/:*?"<>|]', "-", name)
    return name or None


def build_command(url: str, clip_range: tuple[str, str] | None, filename: str | None) -> list[str]:
    output_template = f"{filename}.%(ext)s" if filename else "%(title)s.%(ext)s"

    cmd = [
        "yt-dlp",

        "--extractor-args",
        "youtube:player_client=web_embedded",

        "--no-mtime",
        "-f", FORMAT,
        "--merge-output-format", "mp4",
        "-o", output_template,
    ]

    if clip_range:
        start, end = clip_range
        cmd += [
            "--download-sections", f"*{start}-{end}",
            # keeps the cut frame-accurate without re-downloading the whole video
            "--force-keyframes-at-cuts",
        ]

    cmd.append(url)
    return cmd


def run_download(cmd: list[str]) -> bool:
    print(c("\nDownloading...\n", "cyan"))
    result = subprocess.run(cmd, cwd=DOWNLOAD_PATH)
    return result.returncode == 0


def main() -> None:
    ensure_download_path()

    url = input(f"\nEnter {c('YouTube link', 'red')}: ").strip()

    try:
        extract_video_id(url)
    except ValueError:
        print(c("That doesn't look like a valid YouTube URL.", "red"))
        sys.exit(1)

    video_len = CustomYouTubeAPI.get_video_length(url)
    print(f"Video length: {c(seconds_to_time(video_len), 'cyan')}")

    clip_range = prompt_clip_range(video_len)
    filename = prompt_filename()

    cmd = build_command(url, clip_range, filename)

    if not run_download(cmd):
        print(c("\nDownload failed.", "red"))
        sys.exit(1)

    print(c("\nDone! Video saved as .mp4\n", "green"))


if __name__ == "__main__":
    main()