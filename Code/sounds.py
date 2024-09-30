import pygame as pg
import os
from os.path import join


class Sounds:
    def __init__(self, game):
        self.game = game
        pg.mixer.init()
        self.path = join('Sources', 'sounds',)

        # weapons-sound
        self.shotgun_fire = pg.mixer.Sound(join(self.path, 'weapons', 'shotgun', 'shotgun_fire.wav'))
        self.shotgun_shell_drop = pg.mixer.Sound(join(self.path, 'weapons', 'shotgun', 'shotgun_shell_drop.wav'))
        # self.shotgun_reload = pg.mixer.Sound(join(self.path, 'weapons', 'shotgun', 'shotgun_reload.wav'))
        
        # enemies-sound
        self.attack = pg.mixer.Sound(join(self.path, 'enemy', 'npc_attack.wav'))
        self.death = pg.mixer.Sound(join(self.path, 'enemy', 'npc_death.wav'))
        self.pain = pg.mixer.Sound(join(self.path, 'enemy', 'npc_pain.wav'))
        self.player_pain = pg.mixer.Sound(join(self.path, 'player', 'player_pain.wav'))