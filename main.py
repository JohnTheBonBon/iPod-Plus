# main.py
import time
import requests
import tempfile
import subprocess
from email_processor import EmailProcessor
from tidal_downloader import TidalDownloader
from youtube_downloader import YouTubeDownloader
from ipod_support import iPodSupport
from google_drive_handler import GoogleDriveHandler
from config import Config

def main():
    with tempfile.TemporaryDirectory() as temp_file_dir:
        print(f"Temporary directory path: {temp_file_dir}")
        email_processor = EmailProcessor(Config.MAIL_SERVER, Config.EMAIL_USER, Config.EMAIL_PASS)
        tidal_downloader = TidalDownloader(Config.TIDAL_DL_PATH, temp_file_dir)
        youtube_downloader = YouTubeDownloader(temp_file_dir)
        ipod_support = iPodSupport(temp_file_dir, Config.ITUNES_DIR)
        google_drive_handler = GoogleDriveHandler(temp_file_dir)
        url = None

    while not url:
        try:
            wifi_connected = requests.get("http://www.google.com", timeout=5)
            if wifi_connected.status_code == 200:
                url = email_processor.check_emails()
                if url:
                    subprocess.Popen(["C:/Users/aidda/AppData/Local/Programs/Python/Python312/python.exe", "main.py"])

                    if any("tidal" in u for u in url):

                        tidalDL_success = tidal_downloader.download(url)
                        if tidalDL_success:
                            support_success = ipod_support.convert_and_add_songs()

                            if support_success:
                                google_drive_handler.success_200()
                                google_drive_handler.upload_music_files()
                            else:
                                google_drive_handler.supportFailed_409()

                        else:
                            google_drive_handler.downloadlFailed_408()

                    elif any("youtu.be" in u for u in url):

                        youtubeDL_success = youtube_downloader.download(url)
                        if youtubeDL_success:
                            vidSupport_success = ipod_support.convert_and_add_videos()

                            if  vidSupport_success:
                                google_drive_handler.success_200()
                                google_drive_handler.upload_music_files()
                            else:
                                google_drive_handler.supportFailed_409()

                        else:
                            google_drive_handler.downloadlFailed_408()


                    # email_processor.send_response(url)
                time.sleep(10)
        except (requests.ConnectionError, requests.Timeout) as exception:
            print("No internet connection.")
            time.sleep(120)

if __name__ == "__main__":
    main()
