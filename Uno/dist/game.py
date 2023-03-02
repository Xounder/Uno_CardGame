import pygame, sys
from settings import *
from control import ControlGame
from start_window import StartWindow

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption('UNO')
        self.clock = pygame.time.Clock()

        self.control_game = ControlGame()
        self.start_window = StartWindow(self.control_game.active_game)
        
    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            
            self.screen.fill('blue')

            if not self.control_game.run_game:
                self.start_window.draw()
                self.start_window.update()
            else:
                self.control_game.draw()
                self.control_game.update()

            pygame.display.update()
            self.clock.tick(60)

game = Game()
game.run()