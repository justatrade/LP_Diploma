import os
from decouple import config

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
ACCEPTABLE_FORMATS = ['jpg', 'webp', 'png', 'jpeg', 'tif', 'tiff']
BOT_TOKEN = config('BOT_TOKEN')