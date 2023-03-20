from decouple import config
import os
from recognition.space.space_models import SpaceImage

# Bot
BOT_TOKEN = config('BOT_TOKEN')

# Files
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
SPACE_IMG_PATH = os.path.join('test_img', 'space')
ACCEPTABLE_FORMATS = ['jpg', 'webp', 'png', 'jpeg', 'tif', 'tiff']

# DB
DB_NAME = 'db/space-face.db'

# Space Recognition
FULL_RES_FLAG = False
MIN_CONTOUR_SIZE = 0
USER_CHOICE_MAPPING = {'DwarfWLM': SpaceImage('DwarfGalaxyWLM.png'),
                       'CRICN': SpaceImage('CosmicRiffsInCarinaNebula.png'),
                       'NGC346': SpaceImage('NGC346.png'),
                       'Pandora': SpaceImage('PandoraCluster.png'),
                       'Pillars': SpaceImage('PillarsOfCreation.png'),
                       'Tarantula': SpaceImage('TarantulaNebula.png')}
SPACE_DEBUG_MODE = True
