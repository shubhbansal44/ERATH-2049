# IMPORTS
import pygame as pg
import math
import os

# SCREEN SETTINGS
pg.init()
os.environ['SDL_VIDEO_CENTERED'] = '1'
INFO = pg.display.Info()
# RES = WIDTH, HEIGHT = INFO.current_w, INFO.current_h
RES = WIDTH, HEIGHT = 800, 450
H_WIDTH = WIDTH // 2
H_HEIGHT = HEIGHT // 2
# RES = 1536, 864
FPS = 60

# MAP SETTINGS
DIMENSIONS = (16, 9)
TILE_X = WIDTH / DIMENSIONS[0]
# TILE_X = 100
TILE_Y = HEIGHT / DIMENSIONS[1]
# TILE_Y = 100

# PLAYER SETTINGS
PLAYER_POS = WIDTH / (TILE_X * 2), (HEIGHT - 20) / TILE_Y
PLAYER_ANGLE = 3 * math.pi / 2  # Starting angle (facing down)
PLAYER_SPEED = 2
PLAYER_ROT_SPEED = 2
PLAYER_SCALE = 60

# CONTROL SETTINGS
MOUSE_SENSITIVITY = .3
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