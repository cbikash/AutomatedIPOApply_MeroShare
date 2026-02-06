import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
SECRET_KEY = os.getenv("SECRET_KEY")
DEBUG = os.getenv("DEBUG")
BASE_URL_MEROSHARE= os.getenv('BASE_URL_MEROSHARE')
CLIENT_ID= os.getenv('CLIENT_ID')
CLIENT_SECRET= os.getenv('CLIENT_SECRET')
CLIENT_USERNAME= os.getenv('CLIENT_USERNAME')
CRN= os.getenv('CRN')
PIN= os.getenv('PIN')
