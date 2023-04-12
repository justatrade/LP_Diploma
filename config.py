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
SPACE_DEBUG_MODE = False
SPACE_DEBUG_MODE_TEXT = True

# Overlay
DEFAULT_MATRIX_VALUE = 8
FIRST_CIRCLE_VALUE = DEFAULT_MATRIX_VALUE / 2
SECOND_CIRCLE_VALUE = FIRST_CIRCLE_VALUE / 2
FIRST_CIRCLE = [(-1, 0), (-1, 1), (0, 1), (1, 1),
                (1, 0), (1, -1), (0, -1), (-1, -1)]  # Относительные координаты ближайших 8 точек
SECOND_CIRCLE = [(-2, -2), (-2, -1), (-2, 0), (-2, 1),
                 (-2, 2), (-1, 2), (0, 2), (1, 2),
                 (2, 2), (2, 1), (2, 0), (2, -1),
                 (2, -2), (1, -2), (0, -2), (-1, -2)]  # Относительные координаты точек с удалением 2

