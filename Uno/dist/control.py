import pygame
from player import Player
from table_game import TableGame
from timer import Timer
from settings import screen_width, screen_height
from support import blit_text_shadow

class ControlGame:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.run_game = False
        self.active_timer_once = True
        self.table_game = TableGame()
        # win surface
        win_surf = pygame.image.load('img/win.png').convert()
        self.win_surf = pygame.transform.scale(win_surf, (win_surf.get_width()*2, win_surf.get_height()*2))
        self.win_rect = self.win_surf.get_rect(center= (screen_width/2, screen_height/2))
        # win msg
        self.show_msg_timer = Timer(1.5)
        self.font_win = pygame.font.Font('font/Pixeltype.ttf', 50)

    def active_game(self, qnt_ply, name):
        self.create_players(qnt_ply, name)
        self.run_game = True
        self.active_timer_once = True

    def create_players(self, qnt_ply, name):
        self.players = [Player(name[i]) for i in range(qnt_ply)]
        self.table_game.game_assets(self.players)
        
    def draw(self):
        self.table_game.draw()
        if self.table_game.win:
            if self.show_msg_timer.run:
                self.display_surface.blit(self.win_surf, self.win_rect)
                blit_text_shadow(f'{self.table_game.winner + 1}', 'red', (screen_width/2, screen_height/2), self.font_win, back_color='black')
            else:
                if not self.active_timer_once:
                    self.run_game = False  

    def update(self):
        if self.show_msg_timer.run:
            self.show_msg_timer.update()

        if not self.table_game.win:
            self.table_game.update()
        else:
            if self.active_timer_once:
                self.show_msg_timer.active()
                self.active_timer_once = False