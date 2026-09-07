# IMPORTS
import pygame as pg
from paths import SOUNDS_DIR


class Sounds:
    def __init__(self, game):
        self.game = game
        pg.mixer.init()

        # weapons-sound
        self.shotgun_fire = pg.mixer.Sound(str(SOUNDS_DIR / 'weapons' / 'shotgun' / 'shotgun_fire.wav'))
        self.shotgun_shell_drop = pg.mixer.Sound(str(SOUNDS_DIR / 'weapons' / 'shotgun' / 'shotgun_shell_drop.wav'))
        # self.shotgun_reload = pg.mixer.Sound(str(SOUNDS_DIR / 'weapons' / 'shotgun' / 'shotgun_reload.wav'))
        
        # enemies-sound
        self.attack = pg.mixer.Sound(str(SOUNDS_DIR / 'enemy' / 'npc_attack.wav'))
        self.death = pg.mixer.Sound(str(SOUNDS_DIR / 'enemy' / 'npc_death.wav'))
        self.pain = pg.mixer.Sound(str(SOUNDS_DIR / 'enemy' / 'npc_pain.wav'))
        self.player_pain = pg.mixer.Sound(str(SOUNDS_DIR / 'player' / 'player_pain.wav'))

        # setting-volume
        self.sounds = [self.shotgun_fire, self.shotgun_shell_drop, self.attack, self.death, self.pain, self.player_pain]
        for sound in self.sounds:
            sound.set_volume(.1)
