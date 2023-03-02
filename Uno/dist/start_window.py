import pygame
from timer import Timer
from support import *
from settings import names_input_pos, screen_width, screen_height

class InputText:
    def __init__(self, id, pos, mouse):
        self.display_surface = pygame.display.get_surface()
        self.input_text = pygame.Surface((100, 20))
        self.input_text_rect = self.input_text.get_rect(topleft= (pos))
        self.id = id
        self.text = ''
        self.pressed = False

        self.font = pygame.font.Font('font/Pixeltype.ttf', 25)
        self.timer = Timer(0.12)
        self.mouse_surf = mouse[0]
        self.mouse_rect = mouse[1]

    def draw(self):
        self.display_surface.blit(self.input_text, self.input_text_rect)
        pygame.draw.rect(self.display_surface, 'white', (self.input_text_rect.topleft[0], self.input_text_rect.topleft[1], 100, 20), 1)
        text = [self.text, 'white'] if len(self.text) > 0 else ['insert', 'gray']
        blit_text(text[0], text[1], [self.input_text_rect.center[0], self.input_text_rect.center[1] + 2], self.font)
        blit_text_shadow(f'P{self.id + 1}', 'red', [self.input_text_rect.midleft[0] - 15, self.input_text_rect.midleft[1] + 2], self.font)
    
    def input(self):       
        if pygame.mouse.get_pressed()[0]:
            self.mouse_rect.center = pygame.mouse.get_pos()
            if self.mouse_rect.colliderect(self.input_text_rect):
                self.pressed = True
                self.input_text.fill('red')
            else:
                self.input_text.fill('black')
                self.pressed = False
        if not self.timer.run:
            if self.pressed:
                keys = pygame.key.get_pressed()
                l = ''
                upper = False
                if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT] or keys[pygame.K_CAPSLOCK]:
                        upper = True
                if len(self.text) < 8:
                    if keys[pygame.K_q]:
                        l = 'q'
                    elif keys[pygame.K_w]:
                        l = 'w'
                    elif keys[pygame.K_e]:
                        l = 'e'
                    elif keys[pygame.K_r]:
                        l = 'r'
                    elif keys[pygame.K_t]:
                        l = 't'
                    elif keys[pygame.K_y]:
                        l = 'y'
                    elif keys[pygame.K_u]:
                        l = 'u'
                    elif keys[pygame.K_i]:
                        l = 'i'
                    elif keys[pygame.K_o]:
                        l = 'o'
                    elif keys[pygame.K_p]:
                        l = 'p'
                    elif keys[pygame.K_a]:
                        l = 'a'
                    elif keys[pygame.K_s]:
                        l = 's'
                    elif keys[pygame.K_d]:
                        l = 'd'
                    elif keys[pygame.K_f]:
                        l = 'f'
                    elif keys[pygame.K_g]:
                        l = 'g'
                    elif keys[pygame.K_h]:
                        l = 'h'
                    elif keys[pygame.K_j]:
                        l = 'j'
                    elif keys[pygame.K_k]:
                        l = 'k'
                    elif keys[pygame.K_l]:
                        l = 'l'
                    elif keys[pygame.K_z]:
                        l = 'z'
                    elif keys[pygame.K_x]:
                        l = 'x'
                    elif keys[pygame.K_c]:
                        l = 'c'
                    elif keys[pygame.K_v]:
                        l = 'v'
                    elif keys[pygame.K_b]:
                        l = 'b'
                    elif keys[pygame.K_n]:
                        l = 'n'
                    elif keys[pygame.K_m]:
                        l = 'm'
                    elif keys[pygame.K_0] or keys[pygame.K_KP_0]:
                        l = '0'
                    elif keys[pygame.K_1] or keys[pygame.K_KP_1]:
                        l = '1'
                    elif keys[pygame.K_2] or keys[pygame.K_KP_2]:
                        l = '2'
                    elif keys[pygame.K_3] or keys[pygame.K_KP_3]:
                        l = '3'
                    elif keys[pygame.K_4] or keys[pygame.K_KP_4]:
                        l = '4'
                    elif keys[pygame.K_5] or keys[pygame.K_KP_5]:
                        l = '5'
                    elif keys[pygame.K_6] or keys[pygame.K_KP_6]:
                        l = '6'
                    elif keys[pygame.K_7] or keys[pygame.K_KP_7]:
                        l = '7'
                    elif keys[pygame.K_8] or keys[pygame.K_KP_8]:
                        l = '8'
                    elif keys[pygame.K_9] or keys[pygame.K_KP_9]:
                        l = '9'
                    elif keys[pygame.K_BACKSPACE]:
                        if len(self.text) > 0:
                            self.text = self.text[:len(self.text)-1]
                else:
                    if keys[pygame.K_BACKSPACE]:
                        if len(self.text) > 0:
                            self.text = self.text[:len(self.text)-1]
                self.text += l.upper() if upper else l
                self.timer.active()
    
    def update(self):
        if self.timer.run:
            self.timer.update()
        self.input()

class StartWindow:
    def __init__(self, active_game):
        self.display_surface = pygame.display.get_surface()
        self.back_surf = pygame.image.load('img/start_window.png').convert()
        self.active_game = active_game
        self.qnt_ply = 2

        self.mouse_surf = pygame.Surface((5, 5))
        self.mouse_rect = self.mouse_surf.get_rect(center= (0, 0))
        self.names_input = [InputText(i, (names_input_pos[i]), [self.mouse_surf, self.mouse_rect]) for i in range(12)]

        # collisions
        self.choose_ply_surf = [pygame.Surface((30, 30)) for i in range(2)]
        choose_ply_pos = [[screen_width/2 - 97, screen_height/2 - 17], [screen_width/2 + 95, screen_height/2 - 17]]
        self.choose_ply_rect = [self.choose_ply_surf[i].get_rect(center= (choose_ply_pos[i])) for i in range(2)]
        # start
        self.start_surf = pygame.Surface((194, 66))
        self.start_rect = self.start_surf.get_rect(topleft= (screen_width/2 - 105, screen_height - 85))

        self.timer = Timer(0.2)
        self.font = pygame.font.Font('font/Pixeltype.ttf', 40)

    def clear_names(self):
        for names_input in self.names_input:
            names_input.text = ''

    def draw(self):
        self.display_surface.blit(self.back_surf, (0, 0))
        pygame.draw.rect(self.display_surface, 'blue', (names_input_pos[0][0] - 35, names_input_pos[0][1] - 20, 600, 180))
        pygame.draw.rect(self.display_surface, 'black', (names_input_pos[0][0] - 35, names_input_pos[0][1] - 20, 600, 180), 3)
        pygame.draw.rect(self.display_surface, 'red', (self.start_rect.topleft[0], self.start_rect.topleft[1], 194, 66), 3)
        blit_text_shadow(f'{self.qnt_ply}', 'red', [screen_width/2, screen_height/2 - 17], self.font)
        for i, names_input in enumerate(self.names_input):
            if i + 1 > self.qnt_ply:
                break
            names_input.draw()
    
    def update(self):
        self.input()
        if self.timer.run:
            self.timer.update()
        for i, names_input in enumerate(self.names_input):
            if i + 1 > self.qnt_ply:
                names_input.text = ''
                continue
            names_input.update()
    
    def input(self):
        if not self.timer.run:
            if pygame.mouse.get_pressed()[0]:
                self.mouse_rect.center = pygame.mouse.get_pos()
                if self.mouse_rect.colliderect(self.start_rect):
                    names = [self.names_input[i].text for i in range(self.qnt_ply)]
                    self.active_game(self.qnt_ply, names)
                    self.clear_names()
                else:
                    for i, ch_ply_rect in enumerate(self.choose_ply_rect):
                        if self.mouse_rect.colliderect(ch_ply_rect):
                            if i == 0:
                                self.qnt_ply -= 1 if self.qnt_ply > 2 else 0
                            else:
                                self.qnt_ply += 1 if self.qnt_ply < 12 else 0
                self.timer.active()
