# IMPORTS
import math
from parser import *

# SCREEN SETTINGS
class SCREEN_SETTINGS:
    def __init__(self):
        self.parser = Parser()
        self.RES = self.WIDTH, self.HEIGHT = self.parser.parse_attr('width'), self.parser.parse_attr('height') # 1536, 864
        self.H_WIDTH = self.WIDTH // 2
        self.H_HEIGHT = self.HEIGHT // 2
        self.MAX_FPS = 60


# MAP SETTINGS
class MAP_SETTINGS:
    def __init__(self):
        self.TILE_X = 32
        self.TILE_Y = 33
        self.TILE_DIMENSION_X = 8
        self.TILE_DIMENSION_Y = 8


# PLAYER SETTINGS
class PLAYER_SETTINGS:
    def __init__(self):
        self.parser = Parser()
        self.PLAYER_X, self.PLAYER_Y = self.PLAYER_POS = 13.5, 13.5 # (x-coordinate, y-coordinate)
        self.PLAYER_ANGLE = 3 * math.pi / 2  # Starting angle (facing up)
        self.PLAYER_SPEED = self.parser.parse_attr('player_speed')
        self.PLAYER_ROT_SPEED = self.parser.parse_attr('player_rot_speed')
        self.PLAYER_SCALE = 60
        self.MAX_HEALTH = 1000


# CONTROL SETTINGS
class CONTROL_SETTINGS(SCREEN_SETTINGS):
    def __init__(self):
        super().__init__()
        self.MOUSE_SENSITIVITY = self.parser.parse_attr('mouse_sensitivity')
        self.MOUSE_MAX_RELATIVE = 40
        self.MOUSE_BORDER_LEFT = 10
        self.MOUSE_BORDER_RIGHT = self.WIDTH - self.MOUSE_BORDER_LEFT


# VIEWPORT SETTINGS
class VIEWPORT_SETTINGS(SCREEN_SETTINGS):
    def __init__(self):
        super().__init__()
        self.FOV = math.pi / 3  # Field of view (60 degrees)
        self.H_FOV = self.FOV / 2  # Half of the field of view
        self.CASTED_RAYS = self.WIDTH // 2  # Number of rays to cast
        self.H_CASTED_RAYS = self.CASTED_RAYS // 2  # Half the number of rays
        self.DELTA_ANGLE = self.FOV / self.CASTED_RAYS  # Angle between each ray
        self.MAX_DEPTH = 20  # Max depth for raycasting


# RENDER SETTINGS
class RENDER_SETTINGS(VIEWPORT_SETTINGS):
    def __init__(self):
        super().__init__()
        self.SCREEN_DEPTH = self.H_WIDTH / math.tan(self.H_FOV)  # Distance from the player to the screen
        self.SCALE = self.WIDTH // self.CASTED_RAYS  # Width of each ray slice on screen


# TEXTURE SETTINGS
class TEXTURE_SETTINGS:
    def __init__(self):
        self.TEXTURE_SIZE = 256  # Texture resolution
        self.H_TEXTURE_SIZE = self.TEXTURE_SIZE // 2  # Half of the texture resolution
        self.FLOOR = (30, 30, 30)
        self.DIGIT_SIZE = 60