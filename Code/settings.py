# IMPORTS
import pygame as pg
import math
import os

# SCREEN SETTINGS
pg.init()
os.environ['SDL_VIDEO_CENTERED'] = '1'
INFO = pg.display.Info()
RES = WIDTH, HEIGHT = INFO.current_w, INFO.current_h
# RES = WIDTH, HEIGHT = 800, 450
H_WIDTH = WIDTH // 2
H_HEIGHT = HEIGHT // 2
# RES = 1536, 864
MAX_FPS = 60

# MAP SETTINGS
TILE_X = 32
TILE_Y = 33
TILE_DIMENSION_X = 8
TILE_DIMENSION_Y = 8

# PLAYER SETTINGS
PLAYER_POS = 13.5, 12.5 # (x-coordinate, y-coordinate)
PLAYER_ANGLE = 3 * math.pi / 2  # Starting angle (facing up)
PLAYER_SPEED = 0.004
PLAYER_ROT_SPEED = 0.002
PLAYER_SCALE = 60
MAX_HEALTH = 1000

# CONTROL SETTINGS
MOUSE_SENSITIVITY = .0003
MOUSE_MAX_RELATIVE = 40
MOUSE_BORDER_LEFT = 10
MOUSE_BORDER_RIGHT = WIDTH - MOUSE_BORDER_LEFT

# VIEWPORT SETTINGS
FOV = math.pi / 3  # Field of view (60 degrees)
H_FOV = FOV / 2  # Half of the field of view
CASTED_RAYS = WIDTH // 2  # Number of rays to cast
H_CASTED_RAYS = CASTED_RAYS // 2  # Half the number of rays
DELTA_ANGLE = FOV / CASTED_RAYS  # Angle between each ray
MAX_DEPTH = 20  # Max depth for raycasting

# RENDER SETTINGS
SCREEN_DEPTH = H_WIDTH / math.tan(H_FOV)  # Distance from the player to the screen
SCALE = WIDTH // CASTED_RAYS  # Width of each ray slice on screen

# TEXTURE SETTINGS
TEXTURE_SIZE = 256  # Texture resolution
H_TEXTURE_SIZE = TEXTURE_SIZE // 2  # Half of the texture resolution
FLOOR = (30, 30, 30)
DIGIT_SIZE = 60