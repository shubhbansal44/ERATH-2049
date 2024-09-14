# IMPORTS
import pygame as pg
import math
import os


# SCREEN SETTINGS
pg.init()
os.environ['SDL_VIDEO_CENTERED']='1'
INFO=pg.display.Info()
RES=WIDTH,HEIGHT= INFO.current_w, INFO.current_h
# print(RES) 1536, 864
# RES=WIDTH,HEIGHT= 1280, 720
FPS=60


# PLAYER SETTINGS
PLAYER_POS=WIDTH/2, HEIGHT/2
PLAYER_ANGLE=3*math.pi/2
PLAYER_SPEED=100
PLAYER_ROT_SPEED=2


# MAP SETTINGS
DIMENSIONS=(16, 16)
TILE_DIMENSIONS_X=RES[0]/DIMENSIONS[0]
TILE_DIMENSIONS_Y=RES[1]/DIMENSIONS[1]
# print(TILE_DIMENSIONS_X, TILE_DIMENSIONS_Y) 96, 54


# VIEWPORT SETTINGS
FOV=math.pi/3
H_FOV=FOV/2
CASTED_RAYS=WIDTH//2
H_CASTED_RAYS=CASTED_RAYS//2
DELTA_ANGLE=FOV/CASTED_RAYS
MAX_DEPTH=20