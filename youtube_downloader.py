# youtube_downloader.py
from pytubefix import YouTube
import requests
import time
import os

class YouTubeDownloader:
    def __init__(self, temp_file_dir):
        self.temp_file_dir = temp_file_dir

    def download(self, url):

        try:
            # Download the video
            yt = YouTube(str(url[0]))
            start_timer = time.time()
            stream = yt.streams.get_highest_resolution()
            stream.download(self.temp_file_dir)
            print(f"Downloaded: {yt.title}")

            # Download the thumbnail
            thumbnail_url = yt.thumbnail_url
            response = requests.get(thumbnail_url)
            cover_path = os.path.join(self.temp_file_dir, 'cover.jpg')

            if response.status_code == 200:
                with open(cover_path, 'wb') as file:
                    file.write(response.content)
            print("Thumbnail downloaded successfully!")

            stop_timer = time.time()
            print(f"Time taken: {stop_timer - start_timer} seconds.")
            return True

        except Exception as e:
            print("Error downloading video: ", e)
            return False
