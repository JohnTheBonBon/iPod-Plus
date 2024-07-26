# ipod_support.py
import os
import shutil
import subprocess
import time

class iPodSupport:
    def __init__(self, temp_file_dir, itunes_dir):
        self.temp_file_dir = temp_file_dir
        self.itunes_dir = itunes_dir

    def convert_and_add_songs(self):

        try:
            start_timer = time.time()
            for root, dirs, files in os.walk(self.temp_file_dir):
                for filename in files:
                    if filename.endswith(".flac"):
                        flac_path = os.path.join(root, filename)
                        m4a_file = flac_path.replace('.flac', '.m4a')
                        metadata = [
                            "ffmpeg", "-i", flac_path, "-acodec", "aac", "-b:a", "320k",
                            "-aac_pns", "0", "-map_metadata", "0", "-map", "0", "-c:v", "copy", m4a_file
                        ]
                        subprocess.run(metadata, check=True)
                        shutil.move(m4a_file, self.temp_file_dir)

        except Exception as e:
            print("Error converting song: ", e)
            return False

        #self._clean_temp_files()
        print("Songs added to iTunes.")
        stop_timer = time.time()
        print(f"Time taken: {stop_timer - start_timer} seconds.")
        return True

    def convert_and_add_videos(self):

        try:
            start_timer = time.time()
            for root, dirs, files in os.walk(self.temp_file_dir):
                for filename in files:
                    if filename.endswith(".mp4"):
                        mp4_path = os.path.join(root, filename)
                        mp4_file = os.path.basename(mp4_path).replace('.mp4', '_converted.mp4')
                        metadata = [
                            'ffmpeg', '-i', mp4_path, '-vf', 'scale=320:180', '-r', '30',
                            '-b:v', '600k', '-c:v', 'mpeg4', '-c:a', 'aac', '-ar', '32000',
                            '-ac', '2', '-strict', 'experimental', mp4_file
                        ]
                        subprocess.run(metadata, check=True)
                        shutil.move(mp4_file, self.temp_file_dir)
                        original_name = mp4_file.replace('_converted.mp4', '.mp4')
                        original_path = os.path.join(self.temp_file_dir, original_name)
                        #os.rename(os.path.join(self.temp_file_dir, mp4_file), os.path.join(self.temp_file_dir, original_name))

                        # Delete the old file if it exists
                        if os.path.exists(original_path):
                            os.remove(original_path)

                        # Rename the new file to the old file's name
                        os.rename(os.path.join(self.temp_file_dir, mp4_file), original_path)

        except Exception as e:
            print("Error converting video: ", e)
            return False

        #self._clean_temp_files()
        print("Video added to iTunes.")
        stop_timer = time.time()
        print(f"Time taken: {stop_timer - start_timer} seconds.")
        return True

    def _clean_temp_files(self):
        for filename in os.listdir(self.temp_file_dir):
            file_path = os.path.join(self.temp_file_dir, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print(f'Failed to delete {file_path}. Reason: {e}')
                return False
