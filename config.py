import os
from decouple import config

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
ACCEPTABLE_FORMATS = ['jpg', 'webp', 'png', 'jpeg', 'tif', 'tiff']
BOT_TOKEN = config('BOT_TOKEN')
SPACE_IMG_PATH = os.path.join('test_img', 'space')
DB_NAME = 'db/space-face.db'
