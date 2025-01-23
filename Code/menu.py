# IMPORTS
import pygame as pg
from os.path import join
from parser import Parser
from settings import SCREEN_SETTINGS
from buttons import *


class Menu():
    def __init__(self, game):
        self.game = game
        self.settings()
        self.screen = game.SCREEN
        self.screen_width, self.screen_height = self.screen_settings.WIDTH, self.screen_settings.HEIGHT
        self.get_flags()
        self.get_screens()
        self.flags = {
            'menu': bool,
            'options': bool,
            'load_game': bool,
            'save_game': bool,
            'credits': bool
        }
        self.buttons()

    def get_screens(self):
        self.pause_screen = pg.Surface(self.screen_settings.RES, pg.SRCALPHA)
        self.pause_screen.fill((0, 0, 0, 128))
        self.menu_screen = pg.Surface(self.screen_settings.RES)
        self.menu_screen.fill((45, 53, 62, 255))
        self.credits_text = self.parser.parse_credits(join('Code', 'credits.txt'))
        self.credits_y_offset = self.screen_height

    def get_flags(self):
        self.pause = False
        self.paused = False
        self.menu = True
        self.main_menu = True
        self.options = False
        self.credits = False
        self.load_game = False
        self.save_game = False
        self.settings_saved = False
        self.settings_reset = False
        self.settings_changed = True

    def settings(self):
        self.screen_settings = SCREEN_SETTINGS()
        self.parser = Parser()
        self.saved_settings = self.parser.data

    def update_settings(self):
        self.screen_width, self.screen_height = self.screen_settings.WIDTH, self.screen_settings.HEIGHT
        self.pause_screen = pg.Surface(self.screen_settings.RES, pg.SRCALPHA)
        self.pause_screen.fill((0, 0, 0, 128))
        self.menu_screen = pg.Surface(self.screen_settings.RES)
        self.menu_screen.fill((45, 53, 62, 255))
        self.credits_text = self.parser.parse_credits(join('Code', 'credits.txt'))
        self.credits_y_offset = self.screen_height

    def buttons(self):
        self.all_buttons = []

        # main-menu buttons
        self.new_game_btn = New_Game(self.game, width=15.625, height=6.48, pos=(9.375, 16.67), font_size=1.34)
        self.settings_btn = Settings(self.game, width=15.625, height=6.48, pos=(9.375, 25.926), font_size=1.34)
        self.load_game_btn = Load_Game(self.game, width=15.625, height=6.48, pos=(9.375, 35.19), font_size=1.34)
        self.save_game_btn = Save_Game(self.game, width=15.625, height=6.48, pos=(9.375, 44.45), font_size=1.34)
        self.credits_btn = Credits(self.game, width=15.625, height=6.48, pos=(9.375, 53.71), font_size=1.34)
        self.quit_btn = Quit(self.game, width=15.625, height=6.48, pos=(9.375, 62.97), font_size=1.34)

        # Append main-menu buttons to the list
        self.all_buttons.extend([self.new_game_btn, self.settings_btn, self.load_game_btn, 
                                self.save_game_btn, self.credits_btn, self.quit_btn])

        # options buttons
        self.back_btn = Back(self.game, width=6.25, height=3.71, pos=(1.04, 1.85), font_size=0.85, prev='menu', dynamic_elevation=4)
        self.resolution_btn = Resolution(self.game, width=15.625, height=6.48, pos=(9.375, 16.67), font_size=1.34)
        self.player_speed_btn = Static_Button(self.game, width=15.625, height=6.48, pos=(9.375, 25.926), font_size=1.34, text='Player Speed', dynamic_elevation=0, static_elevation=6, btn_color_3='#475F77')
        self.player_rot_speed_btn = Static_Button(self.game, width=15.625, height=6.48, pos=(9.375, 35.19), font_size=1.34, text='Player Rot Speed', dynamic_elevation=0, static_elevation=6, btn_color_3='#475F77')
        self.mouse_sensitivity_btn = Static_Button(self.game, width=15.625, height=6.48, pos=(9.375, 44.45), font_size=1.34, text='Mouse Sensitivity', dynamic_elevation=0, static_elevation=6, btn_color_3='#475F77')
        self.save_settings_btn = Save_Settings(self.game, width=10.42, height=4.63, pos=(42.71, 53.71), font_size=1)
        self.reset_settings_btn = Reset_Settings(self.game, width=10.42, height=4.63, pos=(55.21, 53.71), font_size=1)

        # Append options buttons to the list
        self.all_buttons.extend([self.back_btn, self.resolution_btn, self.player_speed_btn, 
                                self.player_rot_speed_btn, self.mouse_sensitivity_btn, 
                                self.save_settings_btn, self.reset_settings_btn])

        # additional resolution and control buttons
        self.res1 = Static_Button(self.game, f'{self.parser.default_data["width"]} x {self.parser.default_data["height"]}', 10.42, 4.63, (30.21, 17.13), font='Arial', dynamic_elevation=0, btn_color_3=self.saved_settings['res1'], btn_color_1=self.saved_settings['res1'], static_elevation=4)
        self.res2 = Static_Button(self.game, '1280 x 800', 10.42, 4.63, (42.71, 17.13), font='Arial', dynamic_elevation=0, btn_color_3=self.saved_settings['res2'], static_elevation=4, btn_color_1=self.saved_settings['res2'])
        self.res3 = Static_Button(self.game, '1024 x 768', 10.42, 4.63, (55.21, 17.13), font='Arial', dynamic_elevation=0, btn_color_3=self.saved_settings['res3'], static_elevation=4, btn_color_1=self.saved_settings['res3'])
        self.player_speed = Static_Button(self.game, f'{((self.saved_settings["player_speed"] / 0.006) * 100):.2f}%', 10.42, 4.63, (30.21, 26.34), btn_color_3='#475F77', font='Arial', dynamic_elevation=0, static_elevation=4)
        self.player_speed_down = Down(self.game, width=4.43, height=3.71, pos=(42.71, 27.32), dynamic_elevation=4)
        self.player_speed_up = Up(self.game, width=4.43, height=3.71, pos=(48.70, 27.32), dynamic_elevation=4)
        self.player_rot_speed = Static_Button(self.game, f'{((self.saved_settings["player_rot_speed"] / 0.006) * 100):.2f}%', 10.42, 4.63, (30.21, 35.65), btn_color_3='#475F77', font='Arial', dynamic_elevation=0, static_elevation=4)
        self.player_rot_speed_down = Down(self.game, width=4.43, height=3.71, pos=(42.71, 36.58), dynamic_elevation=4, id=1)
        self.player_rot_speed_up = Up(self.game, width=4.43, height=3.71, pos=(48.70, 36.58), dynamic_elevation=4, id=1)
        self.mouse_sensitivity = Static_Button(self.game, f'{((self.saved_settings["mouse_sensitivity"] / 0.0006) * 100):.2f}%', 10.42, 4.63, (30.21, 44.91), btn_color_3='#475F77', font='Arial', dynamic_elevation=0, static_elevation=4)
        self.mouse_sensitivity_down = Down(self.game, width=4.43, height=3.71, pos=(42.71, 45.84), dynamic_elevation=4, id=2)
        self.mouse_sensitivity_up = Up(self.game, width=4.43, height=3.71, pos=(48.70, 45.84), dynamic_elevation=4, id=2)

        # Append additional buttons to the list
        self.all_buttons.extend([self.res1, self.res2, self.res3, self.player_speed, self.player_speed_down, 
                                self.player_speed_up, self.player_rot_speed, self.player_rot_speed_down, 
                                self.player_rot_speed_up, self.mouse_sensitivity, 
                                self.mouse_sensitivity_down, self.mouse_sensitivity_up])

    def toggle_pause(self):
        self.pause = not self.pause
        self.paused = False
        self.game.game = not self.game.game

    def toggle_menu(self):
        self.menu = not self.menu
        self.main_menu = self.menu
        if not self.game.wasted and not self.game.win:
            self.game.game = not self.game.game

    def draw_pause(self):
        if not self.paused:
            self.screen.blit(self.pause_screen, (0, 0))
            self.paused = True
        pg.display.update()

    def draw_menu(self):
        self.screen.blit(self.menu_screen, (0, 0))
        self.render_text()
        self.new_game_btn.draw()
        self.settings_btn.draw()
        self.load_game_btn.draw()
        self.save_game_btn.draw()
        self.credits_btn.draw()
        self.quit_btn.draw()
        pg.display.update()

    def draw_settings(self):
        self.screen.blit(self.menu_screen, (0, 0))
        self.render_text(text='Settings')
        self.back_btn.draw()
        self.resolution_btn.draw()
        self.res1.draw()
        self.res2.draw()
        self.res3.draw()
        self.player_speed_btn.draw()
        self.player_speed.draw()
        self.player_speed_down.draw()
        self.player_speed_up.draw()
        self.player_rot_speed_btn.draw()
        self.player_rot_speed.draw()
        self.player_rot_speed_down.draw()
        self.player_rot_speed_up.draw()
        self.mouse_sensitivity_btn.draw()
        self.mouse_sensitivity.draw()
        self.mouse_sensitivity_down.draw()
        self.mouse_sensitivity_up.draw()
        self.save_settings_btn.draw()
        self.reset_settings_btn.draw()
        pg.display.update()

    def draw_credits(self):
        self.screen.blit(self.menu_screen, (0, 0))
        self.back_btn.draw()
        credits_y = self.credits_y_offset
        x = (13.02 * self.screen_width) / 100
        for line in self.credits_text:
            self.screen.blit(line, (x, credits_y))
            credits_y += 40
        self.credits_y_offset -= 0.3
        if self.credits_y_offset < -len(self.credits_text) * 40:
            self.credits_y_offset = self.screen_height
        pg.display.update()

    def draw_load_game(self):
        self.screen.blit(self.menu_screen, (0, 0))
        self.render_text(text='Load Game')
        self.back_btn.draw()
        pg.display.update()

    def draw_save_game(self):
        self.screen.blit(self.menu_screen, (0, 0))
        self.render_text(text='Save game')
        self.back_btn.draw()
        pg.display.update()

    def navigate_back(self, prev):
        for flag in self.flags:
            if flag == prev:
                self.flags[flag] = True
            else:
                self.flags[flag] = False
        self.menu = self.flags['menu']
        self.options = self.flags['options']
        self.credits = self.flags['credits']
        self.load_game = self.flags['load_game']
        self.save_game = self.flags['save_game']

    def render_text(self, text='Main Menu', pos=(9.90, 7.41), font='', font_size=2.67, font_color='#FFFFFF'):
        self.font_size_percent = font_size
        self.font_size = int(self.font_size_percent * (self.screen_width + self.screen_height) / 100)
        self.pos_x_percent = pos[0]
        self.pos_y_percent = pos[1]
        self.pos_x = (self.pos_x_percent * self.screen_width) / 100
        self.pos_y = (self.pos_y_percent * self.screen_height) / 100
        font = pg.font.SysFont(font, self.font_size)
        screen_text = font.render(text, True, font_color)
        self.screen.blit(screen_text, (self.pos_x, self.pos_y))
        self.initial_line_pos = (((self.pos_x_percent - 0.52) * self.screen_width) / 100, ((self.pos_y_percent + 5.56) * self.screen_height) / 100)
        self.final_line_pos = (((self.pos_x_percent + 52.08) * self.screen_width) / 100, ((self.pos_y_percent + 5.56) * self.screen_height) / 100)
        pg.draw.line(self.screen, '#000000', self.initial_line_pos, self.final_line_pos, 2)

    def settings_continuity(self):
        if self.menu and not self.options:
            if not self.settings_changed:
                self.saved_settings = self.parser.data
                self.res1.btn_color_1 = self.res1.btn_color_3 = self.saved_settings['res1']
                self.res2.btn_color_1 = self.res2.btn_color_3 = self.saved_settings['res2']
                self.res3.btn_color_1 = self.res3.btn_color_3 = self.saved_settings['res3']
                self.player_speed.text = f'{((self.saved_settings['player_speed'] / 0.006) * 100):.2f}%'
                self.player_rot_speed.text = f'{((self.saved_settings['player_rot_speed'] / 0.006) * 100):.2f}%'
                self.mouse_sensitivity.text = f'{((self.saved_settings['mouse_sensitivity'] / 0.0006) * 100):.2f}%'
                self.resolution_btn.id = self.saved_settings['id']
                self.settings_changed = True

    def draw(self):
        if self.pause:
            self.draw_pause()
        elif self.menu:
            self.draw_menu()
        elif self.options:
            self.draw_settings()
        elif self.credits:
            self.draw_credits()
        elif self.load_game:
            self.draw_load_game()
        elif self.save_game:
            self.draw_save_game()

    def update(self):
        if self.menu:
            self.new_game_btn.function()
            self.settings_btn.function()
            self.load_game_btn.function()
            self.save_game_btn.function()
            self.credits_btn.function()
            self.quit_btn.function()
            self.settings_continuity()
        if self.options:
            self.back_btn.function()
            self.resolution_btn.function()
            self.player_speed_down.function()
            self.player_speed_up.function()
            self.player_rot_speed_down.function()
            self.player_rot_speed_up.function()
            self.mouse_sensitivity_down.function()
            self.mouse_sensitivity_up.function()
            self.save_settings_btn.function()
            self.reset_settings_btn.function()
        if self.credits:
            self.back_btn.function()
        if self.load_game:
            self.back_btn.function()
        if self.save_game:
            self.back_btn.function()
