"""Simple YouTube video downloader script.

Usage:
    python youtube.py <video_url> [output_path]

This uses pytube (https://pytube.io) to download the highest resolution progressive stream.
"""

import sys

from pytube import YouTube


def download_video(url: str, output_path: str = "") -> None:
    """Download a YouTube video from `url` to `output_path` (current dir by default)."""
    yt = YouTube(url)
    # select highest resolution progressive stream
    stream = yt.streams.filter(progressive=True, file_extension="mp4").order_by("resolution").desc().first()
    if not stream:
        raise RuntimeError("No suitable progressive mp4 stream found")

    print(f"Downloading: {yt.title} ({yt.watch_url        # ...existing code...
        yt = YouTube(url)
        # select highest resolution progressive stream
        stream = yt.streams.filter(progressive=True, file_extension="mp4")\
                           .order_by("resolution").desc().first()
        if not stream:
            raise RuntimeError("No suitable progressive mp4 stream found")
    
        # show what we're downloading
        print(f"Downloading: {yt.title} ({yt.watch_url})")
        # usage examples:
        #   python youtube.py https://www.youtube.com/watch?v=voAnXLYqxCw
        #   python youtube.py <url> downloads
        stream.download(output_path=output_path)
        print("Download complete.")
    # ...existing code... youtube.py https://www.youtube.com/watch?v=voAnXLYqxCw
    # or, to save into ./downloads for example:
    python youtube.py https://www.youtube.com/watch?v=voAnXLYqxCw downloads})")
    stream.download(output_path=output_path)
    print("Download complete.")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python youtube.py <url> [output_path]")
        sys.exit(1)

    video_url = sys.argv[1]
    out_dir = sys.argv[2] if len(sys.argv) > 2 else ""

    download_video(video_url, out_dir)
