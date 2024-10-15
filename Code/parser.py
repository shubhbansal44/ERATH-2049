import pygame as pg
from os.path import join
import os
import json


class Parser:
    def __init__(self):
        self.default_settings_path = join('Code', 'default_settings.txt')
        self.saved_settings_path = join('Code', 'saved_settings.txt')
        self.unparse_default_settings()
        self.data = self.parse_settings()

    def parse_settings(self):
        try:
            if os.path.getsize(self.saved_settings_path) > 0:
                with open(self.saved_settings_path, 'r') as settings:
                    data = json.load(settings)
            else:
                raise json.JSONDecodeError("No Saved Settings", self.saved_settings_path, 0)
        except (json.JSONDecodeError, FileNotFoundError):
            with open(self.default_settings_path, 'r') as settings:
                data = json.load(settings)
        return data

    def unparse_default_settings(self):
        pg.init()
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        INFO = pg.display.Info()
        data = {
            "width": INFO.current_w,
            "height": INFO.current_h,
            "player_speed": 0.004,
            "player_rot_speed": 0.002,
            "mouse_sensitivity": 0.0004,
            "res1": "#486a47",
            "res2": "#475F77",
            "res3": "#475F77"
        }
        with open(self.default_settings_path, 'w') as settings:
            json.dump(data, settings)

    def parse_credits(self, path):
        with open(path, 'r') as file:
            credits = file.readlines()
        credits = [line.strip() for line in credits]
        credits_text = []
        font = pg.font.SysFont('', 50, True, False)
        for line in credits:
            credits_line = font.render(line, True, (255, 255, 255))
            credits_text.append(credits_line)
        return credits_text
    
    def parse_attr(self, attribute):
        return self.data[attribute]