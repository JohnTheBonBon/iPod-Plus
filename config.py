# config.py
from decouple import config
from dotenv import load_dotenv

class Config:
    #TEMP_FILE_DIR = "C:/Users/aidda/Documents/iPod-Plus/TempFiles"
    TIDAL_DL_PATH = "C:/Users/aidda/Music/Tidal_Downloader/tidal-dl.exe"
    #ITUNES_DIR = r"C:\Users\aidda\Music\iTunes\iTunes Media\Automatically Add to iTunes"
    DOTENV_PATH = "C:/Users/aidda/Documents/iPod-Plus/config.env"

    load_dotenv(DOTENV_PATH)
    EMAIL_USER = config('EMAIL_USER')
    EMAIL_PASS = config('EMAIL_PASS')
    MAIL_SERVER = config('MAIL_SERVER')
