# IMPORTS
import math
from parser import *


# SCREEN SETTINGS
class SCREEN_SETTINGS():
    RES = None
    WIDTH = None
    HEIGHT = None
    H_HEIGHT = None
    H_WIDTH = None
    MAX_FPS = None

    def __init__(self):
        self.parser = Parser()
        SCREEN_SETTINGS.RES = SCREEN_SETTINGS.WIDTH, SCREEN_SETTINGS.HEIGHT = self.parser.parse_attr('width'), self.parser.parse_attr('height') # 1536, 864
        SCREEN_SETTINGS.H_WIDTH = SCREEN_SETTINGS.WIDTH // 2
        SCREEN_SETTINGS.H_HEIGHT = SCREEN_SETTINGS.HEIGHT // 2
        SCREEN_SETTINGS.MAX_FPS = 60

    def update(self):
        SCREEN_SETTINGS.RES = SCREEN_SETTINGS.WIDTH, SCREEN_SETTINGS.HEIGHT = self.parser.parse_attr('width'), self.parser.parse_attr('height')
        SCREEN_SETTINGS.H_WIDTH = SCREEN_SETTINGS.WIDTH // 2
        SCREEN_SETTINGS.H_HEIGHT = SCREEN_SETTINGS.HEIGHT // 2


# MAP SETTINGS
class MAP_SETTINGS():
    TILE_X = None
    TILE_Y = None
    TILE_DIMENSION_X = None
    TILE_DIMENSION_Y = None

    def __init__(self):
        MAP_SETTINGS.TILE_X = 32
        MAP_SETTINGS.TILE_Y = 33
        MAP_SETTINGS.TILE_DIMENSION_X = 8
        MAP_SETTINGS.TILE_DIMENSION_Y = 8


# PLAYER SETTINGS
class PLAYER_SETTINGS():
    PLAYER_X = None
    PLAYER_POS = None
    PLAYER_Y = None
    PLAYER_ANGLE = None
    PLAYER_SPEED = None
    PLAYER_ROT_SPEED = None
    PLAYER_SCALE = None
    MAX_HEALTH = None

    def __init__(self):
        self.parser = Parser()
        PLAYER_SETTINGS.PLAYER_X, PLAYER_SETTINGS.PLAYER_Y = PLAYER_SETTINGS.PLAYER_POS = 13.5, 13.5 # (x-coordinate, y-coordinate)
        PLAYER_SETTINGS.PLAYER_ANGLE = 3 * math.pi / 2  # Starting angle (facing up)
        PLAYER_SETTINGS.PLAYER_SPEED = self.parser.parse_attr('player_speed')
        PLAYER_SETTINGS.PLAYER_ROT_SPEED = self.parser.parse_attr('player_rot_speed')
        PLAYER_SETTINGS.PLAYER_SCALE = 60
        PLAYER_SETTINGS.MAX_HEALTH = 1000

    def update(self):
        PLAYER_SETTINGS.PLAYER_SPEED = self.parser.parse_attr('player_speed')
        PLAYER_SETTINGS.PLAYER_ROT_SPEED = self.parser.parse_attr('player_rot_speed')


# CONTROL SETTINGS
class CONTROL_SETTINGS():
    MOUSE_SENSITIVITY = None
    MOUSE_MAX_RELATIVE = None
    MOUSE_BORDER_LEFT = None
    MOUSE_BORDER_RIGHT = None

    def __init__(self):
        self.parser = Parser()
        CONTROL_SETTINGS.MOUSE_SENSITIVITY = self.parser.parse_attr('mouse_sensitivity')
        CONTROL_SETTINGS.MOUSE_MAX_RELATIVE = 40
        CONTROL_SETTINGS.MOUSE_BORDER_LEFT = 10
        CONTROL_SETTINGS.MOUSE_BORDER_RIGHT = SCREEN_SETTINGS.WIDTH - CONTROL_SETTINGS.MOUSE_BORDER_LEFT

    def update(self):
        CONTROL_SETTINGS.MOUSE_SENSITIVITY = self.parser.parse_attr('mouse_sensitivity')
        CONTROL_SETTINGS.MOUSE_BORDER_RIGHT = SCREEN_SETTINGS.WIDTH - CONTROL_SETTINGS.MOUSE_BORDER_LEFT
        

# VIEWPORT SETTINGS
class VIEWPORT_SETTINGS():
    FOV = None
    H_FOV = None
    CASTED_RAYS = None
    H_CASTED_RAYS = None
    DELTA_ANGLE = None
    MAX_DEPTH = None

    def __init__(self):
        VIEWPORT_SETTINGS.FOV = math.pi / 3  # Field of view (60 degrees)
        VIEWPORT_SETTINGS.H_FOV = VIEWPORT_SETTINGS.FOV / 2  # Half of the field of view
        VIEWPORT_SETTINGS.CASTED_RAYS = SCREEN_SETTINGS.WIDTH // 2  # Number of rays to cast
        VIEWPORT_SETTINGS.H_CASTED_RAYS = VIEWPORT_SETTINGS.CASTED_RAYS // 2  # Half the number of rays
        VIEWPORT_SETTINGS.DELTA_ANGLE = VIEWPORT_SETTINGS.FOV / VIEWPORT_SETTINGS.CASTED_RAYS  # Angle between each ray
        VIEWPORT_SETTINGS.MAX_DEPTH = 20  # Max depth for raycasting

    def update(self):
        VIEWPORT_SETTINGS.CASTED_RAYS = SCREEN_SETTINGS.WIDTH // 2
        VIEWPORT_SETTINGS.H_CASTED_RAYS = VIEWPORT_SETTINGS.CASTED_RAYS // 2
        VIEWPORT_SETTINGS.DELTA_ANGLE = VIEWPORT_SETTINGS.FOV / VIEWPORT_SETTINGS.CASTED_RAYS

# RENDER SETTINGS
class RENDER_SETTINGS():
    SCREEN_DEPTH = None
    SCALE = None

    def __init__(self):
        RENDER_SETTINGS.SCREEN_DEPTH = SCREEN_SETTINGS.H_WIDTH / math.tan(VIEWPORT_SETTINGS.H_FOV)  # Distance from the player to the screen
        RENDER_SETTINGS.SCALE = SCREEN_SETTINGS.WIDTH // VIEWPORT_SETTINGS.CASTED_RAYS  # Width of each ray slice on screen

    def update(self):
        RENDER_SETTINGS.SCREEN_DEPTH = SCREEN_SETTINGS.H_WIDTH / math.tan(VIEWPORT_SETTINGS.H_FOV)
        RENDER_SETTINGS.SCALE = SCREEN_SETTINGS.WIDTH // VIEWPORT_SETTINGS.CASTED_RAYS

# TEXTURE SETTINGS
class TEXTURE_SETTINGS():
    TEXTURE_SIZE = None
    H_TEXTURE_SIZE = None
    FLOOR = None
    DIGIT_SIZE = None

    def __init__(self):
        TEXTURE_SETTINGS.TEXTURE_SIZE = 256  # Texture resolution
        TEXTURE_SETTINGS.H_TEXTURE_SIZE = TEXTURE_SETTINGS.TEXTURE_SIZE // 2  # Half of the texture resolution
        TEXTURE_SETTINGS.FLOOR = (30, 30, 30)
        TEXTURE_SETTINGS.DIGIT_SIZE = 60
