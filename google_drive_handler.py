# google_drive_handler.py
import os
import glob
import time

import oauth2client.client
import pyautogui
import threading
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

class GoogleDriveHandler:
    def __init__(self, temp_file_dir):
        try:
            self.temp_file_dir = temp_file_dir
            self.gauth = GoogleAuth()
            self.gauth.LoadClientConfigFile('client_secrets.json')
            self.gauth.LoadCredentialsFile("credentials.json")
            self._authenticate()
            self.latest_cycle_number = self.get_latest_cycle_number()
        except Exception as e:
            print("Error initializing GoogleDriveHandler: ", e)
            os.remove("credentials.json")
            self._authenticate()

    def _authenticate(self):
        if self.gauth.credentials is None:
            #auth_thread = threading.Thread(target=self.webAuth)
            #auth_thread.start()
            self.gauth.LocalWebserverAuth()
        elif self.gauth.access_token_expired:
            self.gauth.Refresh()
        else:
            self.gauth.Authorize()
        self.gauth.SaveCredentialsFile("credentials.json")

''''
    def webAuth(self):
        time.sleep(10)

        # click account
        pyautogui.click(1000, 700)
        time.sleep(10)

        # accept verified the app
        pyautogui.click(1270, 700)
        time.sleep(5)

        # trust iPod script
        pyautogui.click(1200, 750)
        time.sleep(5)

        # close browser
        #os.system("taskkill" "C:/Users/aidda/AppData/Local/Programs/Opera/opera.exe")
'''

    def get_latest_cycle_number(self):
        drive = GoogleDrive(self.gauth)
        file_list = drive.ListFile({'q': "trashed=false"}).GetList()
        cycle_numbers = []
        for file in file_list:
            try:
                cycle_number = int(file['title'].split('_')[-1].split('.')[0])
                cycle_numbers.append(cycle_number)
            except ValueError:
                continue
        latest_cycle_number = max(cycle_numbers, default=0)
        return 1 if latest_cycle_number == 5 else latest_cycle_number + 1

    def file_exists(self, filename):
        drive = GoogleDrive(self.gauth)
        file_list = drive.ListFile({'q': f"title='{filename}' and trashed=false"}).GetList()
        return any(file['title'] == filename for file in file_list)

    def start_new_cycle(self):
        self.latest_cycle_number = self.get_latest_cycle_number()

    def create_fileCode(self, filename, content):
        drive = GoogleDrive(self.gauth)
        file = drive.CreateFile({'title': filename})
        file.SetContentString(content)
        file.Upload()
        print('Created file %s with mimeType %s' % (file['title'], file['mimeType']))

    def upload_music_files(self):
        list_of_files = glob.glob(os.path.join(self.temp_file_dir, '**', '*.[mM][pP]4'), recursive=True) + \
                        glob.glob(os.path.join(self.temp_file_dir, '**', '*.[mM]4[aA]'), recursive=True)

        drive = GoogleDrive(self.gauth)

        for file_path in list_of_files:
            file_name = os.path.basename(file_path)
            gfile = drive.CreateFile({'title': file_name, 'parents': [{'id': "1-1QbEGdy_EXW4_F6RbUsWt4Zb-rp2ske"}]})
            gfile.SetContentFile(file_path)
            gfile.Upload()
            print(f'Uploaded file {gfile["title"]} with mimeType {gfile["mimeType"]}')

        print(f"Total files uploaded: {len(list_of_files)}")

    def coverUpload(self):
        filename = f'pic_{self.latest_cycle_number}.jpg'
        content = os.path.join(self.temp_file_dir, 'cover.jpg')

        if not self.file_exists(filename):
            drive = GoogleDrive(self.gauth)
            file = drive.CreateFile({'title': filename})
            file.SetContentFile(content)
            file.Upload()
            print('Created file %s with mimeType %s' % (file['title'], file['mimeType']))

    def success_200(self):
        self.start_new_cycle()
        self.coverUpload()
        filename = f'200_{self.latest_cycle_number}.txt'
        if not self.file_exists(filename):
            self.create_fileCode(filename, '200')

    def downloadlFailed_408(self):
        self.start_new_cycle()
        filename = f'408_{self.latest_cycle_number}.txt'
        if not self.file_exists(filename):
            self.create_fileCode(filename, '408')

    def supportFailed_409(self):
        self.start_new_cycle()
        filename = f'409_{self.latest_cycle_number}.txt'
        if not self.file_exists(filename):
            self.create_fileCode(filename, '409')