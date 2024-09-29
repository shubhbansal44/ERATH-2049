import pygame as pg
from os.path import join


class Sounds:
    def __init__(self, game):
        self.game = game
        pg.mixer.init()
        self.path = join('Sources', 'sounds',)

        # weapons-sound
        self.shotgun_fire = pg.mixer.Sound(join(self.path, 'shotgun', 'shotgun_fire.wav'))
        self.shotgun_shell_drop = pg.mixer.Sound(join(self.path, 'shotgun', 'shotgun_shell_drop.wav'))
        # self.shotgun_reload = pg.mixer.Sound(join(self.path, 'shotgun_reload.wav'))
        
        # enemies-sound
        self.attack = pg.mixer.Sound(join(self.path, 'npc_attack.wav'))
        self.death = pg.mixer.Sound(join(self.path, 'npc_death.wav'))
        self.pain = pg.mixer.Sound(join(self.path, 'npc_pain.wav'))
        self.player_pain = pg.mixer.Sound(join(self.path, 'player_pain.wav'))

