import pygame as pg
from os.path import join
from settings import *
from buttons import *
from parser import *

class Menu():
    def __init__(self, game):
        self.settings()
        self.game = game
        self.screen = game.SCREEN
        self.get_flags()
        self.get_screens()
        self.flags = {
            'menu': bool,
            'options': bool,
            'load_game': bool,
            'save_game': bool,
            'credits': bool
        }
        self.saved_settings = self.parser.parse_settings()
        self.player_speed_value = self.parser.parse_attr('player_speed')
        self.player_rot_speed_value = self.parser.parse_attr('player_rot_speed')
        self.mouse_sensitivity_value = self.parser.parse_attr('mouse_sensitivity')
        self.buttons()

    def get_screens(self):
        self.pause_screen = pg.Surface(self.screen_settings.RES, pg.SRCALPHA)
        self.pause_screen.fill((0, 0, 0, 128))
        self.menu_screen = pg.Surface(self.screen_settings.RES)
        self.menu_screen.fill((45, 53, 62, 255))
        self.credits_text = self.screen_settings.parser.parse_credits(join('Code', 'credits.txt'))
        self.credits_y_offset = self.screen_settings.HEIGHT

    def get_flags(self):
        self.pause = False
        self.paused = False
        self.menu = True
        self.main_menu = True
        self.options = False
        self.credits = False
        self.load_game = False
        self.save_game = False

    def settings(self):
        self.screen_settings = SCREEN_SETTINGS()
        self.parser = Parser()

    def buttons(self):
        self.new_game_btn = New_Game(self.game, width=300, height=70, pos=(180, 180), font_size=40)
        self.settings_btn = Settings(self.game, width=300, height=70, pos=(180, 280), font_size=40)
        self.load_game_btn = Load_Game(self.game, width=300, height=70, pos=(180, 380), font_size=40)
        self.save_game_btn = Save_Game(self.game, width=300, height=70, pos=(180, 480), font_size=40)
        self.credits_btn = Credits(self.game, width=300, height=70, pos=(180, 580), font_size=40)
        self.quit_btn = Quit(self.game, width=300, height=70, pos=(180, 680), font_size=40)
        self.back_btn = Back(self.game, width=120, height=40, pos=(20, 20), font_size=25, prev='menu', dynamic_elevation=4)
        self.resolution_btn = Resolution(self.game, width=300, height=70, pos=(180, 180), font_size=40)
        self.player_speed_btn = Static_Button(self.game, width=300, height=70, pos=(180, 280), font_size=40, text='Player Speed', dynamic_elevation=0, static_elevation=6, btn_color_3='#475F77')
        self.player_rot_speed_btn = Static_Button(self.game, width=300, height=70, pos=(180, 380), font_size=40, text='Player Rot Speed', dynamic_elevation=0, static_elevation=6, btn_color_3='#475F77')
        self.mouse_sensitivity_btn = Static_Button(self.game, width=300, height=70, pos=(180, 480), font_size=40, text='Mouse Sensitivity', dynamic_elevation=0, static_elevation=6, btn_color_3='#475F77')
        self.save_settings_btn = Save_Settings(self.game, width=300, height=70, pos=(180, 580), font_size=40)
        self.res1 = Static_Button(self.game, f'{self.parser.parse_attr('width')} x {self.parser.parse_attr('height')}', 200, 50, (580, 185), font='Arial', dynamic_elevation=0, btn_color_3='#486a47', btn_color_1='#486a47', static_elevation=4)
        self.res2 = Static_Button(self.game, '1280 x 800', 200, 50, (820, 185), font='Arial', dynamic_elevation=0, btn_color_3='#475F77', static_elevation=4)
        self.res3 = Static_Button(self.game, '1024 x 768', 200, 50, (1060, 185), font='Arial', dynamic_elevation=0, btn_color_3='#475F77', static_elevation=4)
        self.player_speed = Static_Button(self.game, f'{((self.player_speed_value / 0.006) * 100):.2f}%', 200, 50, (580, 285), btn_color_3='#475F77', font='Arial', dynamic_elevation=0, static_elevation=4)
        self.player_speed_down = Down(self.game, width=85, height=40, pos=(820, 295), dynamic_elevation=4)
        self.player_speed_up = Up(self.game, width=85, height=40, pos=(935, 295), dynamic_elevation=4)
        self.player_rot_speed = Static_Button(self.game, f'{((self.player_rot_speed_value / 0.006) * 100):.2f}%', 200, 50, (580, 385), btn_color_3='#475F77', font='Arial', dynamic_elevation=0, static_elevation=4)
        self.player_rot_speed_down = Down(self.game, width=85, height=40, pos=(820, 395), dynamic_elevation=4, attr='player_rot_speed')
        self.player_rot_speed_up = Up(self.game, width=85, height=40, pos=(935, 395), dynamic_elevation=4, attr='player_rot_speed')
        self.mouse_sensitivity = Static_Button(self.game, f'{((self.mouse_sensitivity_value / 0.0006) * 100):.2f}%', 200, 50, (580, 485), btn_color_3='#475F77', font='Arial', dynamic_elevation=0, static_elevation=4)
        self.mouse_sensitivity_down = Down(self.game, width=85, height=40, pos=(820, 495), dynamic_elevation=4, attr='mouse_sensitivity')
        self.mouse_sensitivity_up = Up(self.game, width=85, height=40, pos=(935, 495), dynamic_elevation=4, attr='mouse_sensitivity')


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
        self.render_text(pos=(190, 80), font_size=80)
        self.new_game_btn.draw()
        self.settings_btn.draw()
        self.load_game_btn.draw()
        self.save_game_btn.draw()
        self.credits_btn.draw()
        self.quit_btn.draw()
        pg.display.update()

    def draw_settings(self):
        self.screen.blit(self.menu_screen, (0, 0))
        self.render_text(pos=(190, 80), font_size=80, text='Settings')
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
        pg.display.update()

    def draw_credits(self):
        self.screen.blit(self.menu_screen, (0, 0))
        self.back_btn.draw()
        credits_y = self.credits_y_offset
        for line in self.credits_text:
            self.screen.blit(line, (250, credits_y))
            credits_y += 40
        self.credits_y_offset -= 0.3
        if self.credits_y_offset < -len(self.credits_text) * 40:
            self.credits_y_offset = self.screen_settings.HEIGHT
        pg.display.update()

    def draw_load_game(self):
        self.screen.blit(self.menu_screen, (0, 0))
        self.render_text(pos=(190, 80), font_size=80, text='Load Game')
        self.back_btn.draw()
        pg.display.update()

    def draw_save_game(self):
        self.screen.blit(self.menu_screen, (0, 0))
        self.render_text(pos=(190, 80), font_size=80, text='Save game')
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

    def render_text(self, text='Main Menu', pos=(100, 100), font='', font_size=30, font_color='#FFFFFF', flag=True):
        font = pg.font.SysFont(font, font_size)
        screen_text = font.render(text, True, font_color)
        self.screen.blit(screen_text, pos)
        if flag:
            pg.draw.line(self.screen, '#000000', (pos[0] - 10, pos[1] + 60), (pos[0] + 1000, pos[1] + 60), 2)

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
        # print(f'main menu: {self.main_menu}\nmenu: {self.menu}\nsettings: {self.options}\ncredits: {self.credits}\nload game: {self.load_game}\nsave game: {self.save_game}')
        if self.menu:
            self.new_game_btn.function()
            self.settings_btn.function()
            self.load_game_btn.function()
            self.save_game_btn.function()
            self.credits_btn.function()
            self.quit_btn.function()
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
        if self.credits:
            self.back_btn.function()
        if self.load_game:
            self.back_btn.function()
        if self.save_game:
            self.back_btn.function()