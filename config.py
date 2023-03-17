from decouple import config
import recognition.space.space_models as sm
import os

# Bot
BOT_TOKEN = config('BOT_TOKEN')

# Files
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
SPACE_IMG_PATH = os.path.join('test_img', 'space')
ACCEPTABLE_FORMATS = ['jpg', 'webp', 'png', 'jpeg', 'tif', 'tiff']

# DB
DB_NAME = 'db/space-face.db'

# Space Recognition
MIN_CONTOUR_SIZE = 0
USER_CHOICE_MAPPING = {'DwarfWLM': sm.DwarfWLM(), 'CRICN': sm.CRICN(),
                       'NGC346': sm.NGC346(), 'Pandora': sm.Pandora(),
                       'Pillars': sm.Pillars(), 'Tarantula': sm.Tarantula()}
SPACE_DEBUG_MODE = False
