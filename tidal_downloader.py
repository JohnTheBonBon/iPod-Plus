# tidal_downloader.py
import os
import sys
import time
import pexpect
import pexpect.popen_spawn
from mutagen.flac import FLAC

class TidalDownloader:
    def __init__(self, tidal_dl_path, temp_file_dir):
        self.tidal_dl_path = tidal_dl_path
        self.temp_file_dir = temp_file_dir

    def extract_cover_art(self, file_path):
        audio = FLAC(file_path)

        if audio.pictures:
            artwork = audio.pictures[0].data # extract artwork
            cover_path = os.path.join(self.temp_file_dir, 'cover.jpg')
            print(cover_path)
            with open(cover_path, "wb") as img:
                img.write(artwork)

    def download(self, url):
        print("Downloading songs... has begun.")
        start_timer = time.time()
        pex = pexpect.popen_spawn.PopenSpawn(self.tidal_dl_path)
        pex.expect("Enter Choice:")
        pex.sendline("4")

        pex.sendline(self.temp_file_dir)
        pex.sendline("0")
        pex.sendline("0")
        pex.sendline("0")
        pex.sendline("0")

        pex.expect("Enter Choice:")
        pex.sendline(str(url[0]))

        while True:
            for root, dirs, files in os.walk(self.temp_file_dir):
                if any(file.endswith('.flac') for file in files):
                    next(os.path.join(root, file) for file in files if file.endswith('.flac'))
                    break
            else:
                time.sleep(1)
                continue
            break

        pex.sendline("0")
        try:
            pex.expect(pexpect.popen_spawn.EOF, timeout=390)
        except pexpect.exceptions.TIMEOUT:
            print("Download timed out.")
            return False

        time.sleep(10)
        for root, dirs, files in os.walk(self.temp_file_dir):
            for file in files:
                if file.endswith('.flac'):  # check for FLAC files
                    self.extract_cover_art(os.path.join(root, file))
                    break  # stop after first file
            else:
                continue  # executed if the loop ended normally (no break)
            break  # executed if 'continue' was skipped (break)

        print("Download complete.")
        stop_timer = time.time()
        print(f"Time taken: {stop_timer - start_timer} seconds.")
        return True
