import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    account = os.getenv("ACCOUNT")
    password = os.getenv("PASSWORD")
    download_directory = os.getenv("DOWNLOAD_DIRECTORY")
    data_output = os.getenv("DATA_OUTPUT")
    excel_link = os.getenv("EXCEL_LINK")


settings = Settings()
