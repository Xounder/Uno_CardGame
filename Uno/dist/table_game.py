import pygame
from settings import *
from random import randint
from player import Player
from timer import Timer
from support import *

class TableGame:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.players = None
        self.atual_player = None
        self.id_player = 0
        self.show_player_cards = False
        self.show_qnt_buy = [0, False]
        self.win = False
        self.winner = 0
        self.cards_table = [] 
        self.last_card = None
        self.last_card_img = None
        
        self.qnt_block = 0
        self.qnt_reverse = 0
        self.qnt_buy = 0
        self.next_ply_pass = False
        self.cnt_clockwise = True
        self.change_color = False
        self.trade_card = False
        self.cards_name = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'reverse', '+2', 'block']
        self.gray_cards_name = ['+4', 'change']
        #####
        background = pygame.image.load('img/background.jpg').convert() # <- site: https://wallpapercave.com/wood-wallpapers
        self.background = pygame.transform.scale(background, (screen_width, screen_height))
        self.background_rect = self.background.get_rect(topleft= (0, 0))
        # table player
        table_player = pygame.image.load('img/baixo.png').convert()
        self.table_ply = pygame.transform.scale(table_player, (screen_width, table_player.get_height()))
        self.table_ply_rect = self.table_ply.get_rect(topleft= (0, screen_height - self.table_ply.get_height())) 
        # buy_cards table
        buy_cards_surf = pygame.image.load('img/cards/back.png').convert()
        self.buy_cards_surf = pygame.transform.scale(buy_cards_surf, (tile_size[0], tile_size[1]))
        self.buy_cards_rect = self.buy_cards_surf.get_rect(center = (screen_width/2, screen_height/2 - 200))
        # cards table
        self.card_table_surf = None
        self.card_table_rect = None
        # collisions
        y_pos = screen_height - self.table_ply.get_height() + 10
            # pass
        self.pass_surf = pygame.image.load('img/pass.png').convert()
        self.pass_rect = self.pass_surf.get_rect(topleft= (12, y_pos + 2))
            # choose card
        self.choose_card_surf = [pygame.Surface((tile_size[0]+5, tile_size[1]+5)) for i in range(7)]
        self.choose_card_rect = [self.choose_card_surf[i].get_rect(topleft= (155 + (i*86), y_pos - 2)) for i in range(7)]
            # next section
        next_section_surf = pygame.image.load('img/next.png')
        self.next_section_surf = pygame.transform.scale(next_section_surf, (35, 35))
        self.next_section_rect = self.next_section_surf.get_rect(topleft= (screen_width - 42, y_pos + 30))
            # previous section
        self.prev_section_surf = pygame.transform.rotate(self.next_section_surf, 180)
        self.prev_section_rect = self.prev_section_surf.get_rect(topleft= (110, y_pos + 30))
            # show card
        self.show_cards_img = [pygame.image.load('img/show0.png').convert(), pygame.image.load('img/show1.png').convert()]
        self.show_cards_surf = self.show_cards_img[0]
        self.show_cards_rect = self.show_cards_surf.get_rect(topleft= (screen_width - 35, y_pos))

        # change_color
        change_color_surf = pygame.image.load('img/change.png').convert()
        self.change_color_surf = pygame.transform.scale(change_color_surf, (tile_size[0]*2, tile_size[1]*2))
        self.change_color_rect = self.change_color_surf.get_rect(center= (screen_width/2, screen_height/2 - 50))
        self.change_colision_surf = [pygame.Surface((55, 55)) for i in range(4)]
        change_colision_pos = [[screen_width/2 - 60, screen_height/2 - 90], [screen_width/2, screen_height/2 - 90], [screen_width/2 - 60, screen_height/2 - 30], [screen_width/2, screen_height/2 - 30]]
        self.change_colision_rect = [self.change_colision_surf[i].get_rect(topleft= (change_colision_pos[i])) for i in range(4)]

        # trade card
        self.trade_collisions = None
        self.trade_coll_pos = [[screen_width/2 - 170, screen_height/2 - 100], [screen_width/2 - 83, screen_height/2 - 100],
                               [screen_width/2 + 3, screen_height/2 - 100], [screen_width/2 + 90, screen_height/2 - 100],
                               [screen_width/2 - 170, screen_height/2 - 40], [screen_width/2 - 83, screen_height/2 - 40],
                               [screen_width/2 + 3, screen_height/2 - 40], [screen_width/2 + 90, screen_height/2 - 40],
                               [screen_width/2 - 170, screen_height/2 + 20], [screen_width/2 - 83, screen_height/2 + 20],
                               [screen_width/2 + 3, screen_height/2 + 20], [screen_width/2 + 90, screen_height/2 + 20]]
        self.trade_coll_rect = None
        self.trade_cancel_coll = pygame.Surface((120, 50))
        self.trade_cancel_rect = self.trade_cancel_coll.get_rect(topleft = (screen_width/2 - 65, screen_height/2 + 75))

        # mouse
        self.mouse_surf = pygame.Surface((5,5))
        self.mouse_rect = self.mouse_surf.get_rect(center= (0, 0))
        # timer
        self.mouse_timer = Timer(0.5)
        self.show_name_timer = Timer(0.7)
        # font
        self.font = pygame.font.Font('font/Pixeltype.ttf', 40)

    def game_assets(self, players:Player):
        self.all_cards = uno_cards[:]
        self.players = players
        self.id_player = 0
        self.atual_player = self.players[self.id_player]
        self.show_player_cards = False
        self.show_qnt_buy = [0, False]
        self.win = False
        self.winner = 0
        self.distribuition_cards()
        self.import_cards_assets()
        self.cards_table = [self.buy_first_card()] 
        self.last_card = self.cards_table[0][:]
        self.last_card_img = self.last_card[:]
        self.card_table_surf = self.return_card_img(self.last_card_img[1], self.last_card_img[0])
        self.card_table_rect = self.card_table_surf.get_rect(center= (screen_width/2, screen_height/2 - 50))
        # trade - card
        self.trade_collisions = [pygame.Surface((80, 50)) for i in range(len(self.players))]
        self.trade_coll_rect = [self.trade_collisions[i].get_rect(topleft = (self.trade_coll_pos[i])) for i in range(len(self.players))]
        self.show_name_timer.active()

    def distribuition_cards(self):
        for player in self.players:
            for j in range(7):
                player.buy_card(self.buy_card())
    
    def import_cards_assets(self):
        self.cards_surf = {'red': [], 'green': [], 'yellow': [], 'blue': [], 'gray': []}
        for key in self.cards_surf:
            if key == 'gray':
                cards_surf = [pygame.image.load(f'img/cards/{key}/{gray_card_name}.png').convert() for gray_card_name in self.gray_cards_name]
                self.cards_surf[key] = [pygame.transform.scale(cards_surf[i], (tile_size[0], tile_size[1])) for i in range(len(self.gray_cards_name))]
            else:
                cards_surf = [pygame.image.load(f'img/cards/{key}/{card_name}.png').convert() for card_name in self.cards_name]
                self.cards_surf[key] = [pygame.transform.scale(cards_surf[i], (tile_size[0], tile_size[1])) for i in range(len(self.cards_name))]

    def buy_first_card(self):
        card_denied = ['+4', 'reverse', 'block', '+2', 'change']
        for i in range(50):
            choosed = randint(0, len(self.all_cards)-1)
            card = self.all_cards[choosed][:]
            if card_denied.count(card[0]) == 0:
                self.all_cards.pop(choosed)
                return card

    def buy_card(self):
        choosed = randint(0, len(self.all_cards)-1)
        card = self.all_cards[choosed][:]
        self.all_cards.pop(choosed)
        if len(self.all_cards) == 0:
           self.replace_all_cards()
        return card

    def replace_all_cards(self):
        # retorna as cartas para a buy_mesa 
        last_table_card = self.cards_table[len(self.cards_table)-1][:]
        self.cards_table.pop(len(self.cards_table)-1)
        self.all_cards = self.cards_table[:]
        self.cards_table = [last_table_card[:]]

    def next_player(self): # ajustar 
        # passa para o proximo player
        self.show_player_cards = False
        self.show_cards_surf = self.show_cards_img[0]
        self.atual_player.can_buy = True
        self.show_qnt_buy = [0, False]
        if not self.check_win():
            self.atual_player.section = 0
            if len(self.players) == 2:
                if self.qnt_block == 0:
                    self.adjust_id_player()       
            else:
                if self.cnt_clockwise and self.qnt_reverse%2 != 0:
                    self.cnt_clockwise = False
                elif not self.cnt_clockwise and self.qnt_reverse%2 != 0:
                    self.cnt_clockwise = True
                self.adjust_id_player()

            self.atual_player = self.players[self.id_player]
            self.qnt_reverse = 0
            self.qnt_block = 0
            if self.qnt_buy > 0:
                if not self.player_have_buy_card(True if self.next_ply_pass else False):
                    self.show_qnt_buy = [self.qnt_buy, True]
                    for i in range(self.qnt_buy):
                        self.atual_player.buy_card(self.buy_card())
                    if self.next_ply_pass:
                        self.change_color = True
                        self.next_ply_pass = False
                    self.qnt_buy = 0
            if not self.change_color:
                self.show_name_timer.active()

    def adjust_id_player(self): #ajustar (clock_wise*)
        if len(self.players) == 2:
            self.id_player = (self.id_player + 1) % 2
        else:
            if self.cnt_clockwise: #0, 1, 2, 3, 4...
                self.id_player += self.qnt_block % len(self.players)
                if self.id_player < len(self.players)-1:
                    self.id_player += 1
                else:
                    self.id_player = 0 + ((len(self.players)-1) - self.id_player)
            else:
                self.id_player -= self.qnt_block % len(self.players)
                if self.id_player > 0:
                    self.id_player -= 1
                else:
                    self.id_player = (len(self.players)-1) + self.id_player
    
    def player_have_buy_card(self, buy_4):
        if buy_4 and self.atual_player.cards.count(['+4', 'gray']) > 0:
            return True
        elif not buy_4 and (self.atual_player.cards.count(['+2', 'red']) > 0 or
                             self.atual_player.cards.count(['+2', 'blue']) > 0 or 
                                self.atual_player.cards.count(['+2', 'green']) > 0 or 
                                    self.atual_player.cards.count(['+2', 'yellow']) > 0 or
                                        self.atual_player.cards.count(['+4', 'gray']) > 0):
            return True
        return False

    def check_win(self):
        # verifica se o atual jogador venceu
        if self.atual_player.get_qnt_cards() == 0:
            self.win = True
            self.winner = self.id_player
            return True
        return False

    def input(self):
        if not self.mouse_timer.run:
            if pygame.mouse.get_pressed()[0]:
                self.mouse_rect.center = pygame.mouse.get_pos()
                if self.change_color:
                    card = [['', 'red'], ['', 'blue'], ['', 'green'], ['', 'yellow']]
                    for i, change_coll in enumerate(self.change_colision_rect):
                        if self.mouse_rect.colliderect(change_coll):
                            self.last_card = card[i][:]
                            self.change_color = False
                            self.next_player()
                            break
                elif not self.show_player_cards:
                    if self.mouse_rect.colliderect(self.show_cards_rect):
                        self.show_player_cards = not self.show_player_cards
                        self.show_cards_surf = self.show_cards_img[self.show_player_cards]
                elif self.trade_card:
                    if self.mouse_rect.colliderect(self.trade_cancel_rect):
                        self.trade_card = False
                        self.next_player()
                    else:
                        for i, trade_coll in enumerate(self.trade_coll_rect):
                            if i != self.id_player and self.mouse_rect.colliderect(trade_coll):
                                self.trade_players_card(id_ply= i)
                                self.trade_card = False
                                self.next_player()
                                break
                else:
                    if not self.atual_player.can_buy and self.mouse_rect.colliderect(self.pass_rect):
                        self.next_player()
                    elif self.atual_player.can_buy and self.mouse_rect.colliderect(self.buy_cards_rect):
                        self.atual_player.buy_card(self.buy_card())      
                        self.atual_player.can_buy = False
                    elif (self.atual_player.section + 1) * 7 < len(self.atual_player.cards) and self.mouse_rect.colliderect(self.next_section_rect):
                                self.atual_player.section += 1
                    elif self.atual_player.section > 0 and self.mouse_rect.colliderect(self.prev_section_rect):
                        self.atual_player.section -= 1
                    elif self.atual_player.get_qnt_chcards() > 0 and self.mouse_rect.colliderect(self.card_table_rect):
                        self.add_card_table()
                    else:
                        self.choose_card()      
                self.mouse_timer.active()

    def add_card_table(self):
        # adiciona a peça jogada (pelo player) a mesa
        for choose_card in self.atual_player.choose_cards:
            card = self.atual_player.get_card(choose_card)
            if card[0] == 'block':
                self.qnt_block += 1
            elif card[0] == 'reverse':
                self.qnt_reverse += 1
            elif card[0] == '+2':
                self.qnt_buy += 2
            elif card[0] == '+4':
                self.qnt_buy += 4
                self.next_ply_pass = True
            self.cards_table.append(card[:]) 
        # remove cards
        ord_card = self.atual_player.choose_cards[:]
        ord_card.sort(reverse=True)
        for index_card in ord_card:
            self.atual_player.remove_card(index_card)

        self.last_card = card[:]
        self.last_card_img = self.last_card[:]
        self.atual_player.reset_chcards()
        if card[0] == 'change':
            self.change_color = True
        elif card[0] == '0':
            self.trade_card = True
        else:
            self.next_player()

    def trade_players_card(self, id_ply):
        aux_card = self.atual_player.cards[:]
        self.atual_player.cards = self.players[id_ply].cards[:]
        self.players[id_ply].cards = aux_card[:]

    def choose_card(self):
        # o player escolhe a peça desejada
        for i, choose_card in enumerate(self.atual_player.choose_cards):
            index = choose_card - (7 * self.atual_player.section)
            if 0 <= index <= 6:
                if self.mouse_rect.colliderect(self.choose_card_rect[index]):
                    self.atual_player.remove_choose_card(i)
                    return

        len_cards = (len(self.atual_player.cards)-1) - (7 * self.atual_player.section)
        for i, cards_rect in enumerate(self.choose_card_rect):
            if i <= len_cards and self.mouse_rect.colliderect(cards_rect):
                index = i + (7 * self.atual_player.section)
                if self.check_choose_card(self.atual_player.get_card(index)):
                    self.atual_player.choose_cards.append(index) 
                    return
    
    def is_playable(self, card):
        # verifica se a peça pode ser jogada ou não
        if self.qnt_buy > 0:
            if (not self.next_ply_pass and (card[0] == '+2' or card[0] == '+4')) or (self.next_ply_pass and card[0] == '+4'):
                return True
        elif card[1] == 'gray' or card[0] == self.last_card[0] or card[1] == self.last_card[1]:
            return True
        return False
    
    def is_sequential_card(self, card, last_ply_card):
        # verifica os numeros se combinam em NUM ou em COR+(NUM+-1)
        last_num = int(last_ply_card[0]) if last_ply_card[0].isnumeric() else last_ply_card[0]
        atual_num = int(card[0] )if card[0].isnumeric() else card[0]
        if atual_num == last_num or (card[1] == last_ply_card[1] and (atual_num + 1 == last_num or atual_num - 1 == last_num)):
            return True
        return False

    def check_choose_card(self, card):
        if self.atual_player.get_qnt_chcards() > 0:
            if card[1] == 'gray':
                if card[0] == '+4':
                    if self.atual_player.get_last_chcard()[0] == '+2' or self.atual_player.get_last_chcard()[0] == '+4':
                        return True
                else:
                    if self.atual_player.get_last_chcard()[0] == 'change':
                        return True
                return False
            else:
                if card[0] == 'reverse':
                    if self.atual_player.get_last_chcard()[0] == 'reverse':
                        return True
                elif card[0] == 'block':
                    if self.atual_player.get_last_chcard()[0] == 'block':
                        return True
                elif card[0] == '+2':
                    if self.atual_player.get_last_chcard()[0] == '+2':
                        return True
                else:
                    return self.is_sequential_card(card, self.atual_player.get_last_chcard())
                return False
        else:
            return self.is_playable(card)

    def update(self):
        if self.mouse_timer.run:
            self.mouse_timer.update()
        if self.show_name_timer.run:
            self.show_name_timer.update()
        self.input()

    def return_card_img(self, key, name):
        if key == 'gray':
            index = self.gray_cards_name.index(name)
        else:
            index = self.cards_name.index(name)
        return self.cards_surf[key][index]

    def draw_ply_cards(self, section_cards):
        y_pos = screen_height - self.table_ply.get_height() + 10
        for i, card in enumerate(section_cards):
            x_pos = 155 + (i * 86)
            choosed = False
            # background card
            if len(self.atual_player.choose_cards) > 0:
                if self.atual_player.choose_cards.count((7 * self.atual_player.section) + i) > 0:
                    color = 'red'
                    choosed = True
                else:
                    color = 'white'
            else: 
                color = 'green' if self.is_playable(card) else 'white' 
            self.choose_card_surf[i].fill(color)
            self.display_surface.blit(self.choose_card_surf[i], self.choose_card_rect[i])
            # card
            card_surf = self.return_card_img(card[1], card[0])
            if choosed:
                self.display_surface.blit(card_surf, (x_pos + 2, y_pos - 10)) 
            else:
                self.display_surface.blit(card_surf, (x_pos + 2, y_pos)) 
                
    def draw_bottom_elements(self):
        # desenha a parte inferior da tela
        self.display_surface.blit(self.table_ply, self.table_ply_rect)
        self.display_surface.blit(self.pass_surf, self.pass_rect)
        # player cards
        if self.show_player_cards:
            limit_cards = [self.atual_player.section * 7, (self.atual_player.section + 1) * 7]
            if limit_cards[1] > len(self.atual_player.cards):
                limit_cards = [self.atual_player.section * 7, len(self.atual_player.cards)]
            section_cards = self.atual_player.cards[limit_cards[0]:limit_cards[1]]
            self.draw_ply_cards(section_cards)
            # next//previous section
            if (self.atual_player.section + 1) * 7 < len(self.atual_player.cards):
                self.display_surface.blit(self.next_section_surf, self.next_section_rect)
            if self.atual_player.section > 0:
                self.display_surface.blit(self.prev_section_surf, self.prev_section_rect)
        # show//player_id
        self.display_surface.blit(self.show_cards_surf, self.show_cards_rect)
        blit_text_shadow(f'P{self.id_player + 1}', 'red', (screen_width - 23, screen_height - 15), self.font)
        blit_text_shadow(f'+{self.show_qnt_buy[0]}' if self.show_qnt_buy[1] else '', 'red', (130, screen_height - 15), self.font)
        blit_text_shadow(f'{self.atual_player.get_qnt_cards()}', 'red', (130, screen_height - 90), self.font)
        pygame.draw.rect(self.display_surface, 'black', [115, screen_height - 105, 25, 25], 2)

    def draw_table_elements(self):
        self.card_table_surf = self.return_card_img(self.last_card_img[1], self.last_card_img[0])
        self.display_surface.blit(self.card_table_surf, self.card_table_rect)
        self.display_surface.blit(self.buy_cards_surf, self.buy_cards_rect)

    def draw_atual_player_name(self):
        pygame.draw.rect(self.display_surface, 'gray', (screen_width/2 - 100, screen_height/2 - 70, 200, 50))
        pygame.draw.rect(self.display_surface, 'black', (screen_width/2 - 100, screen_height/2 - 70, 200, 50), 3)
        pygame.draw.rect(self.display_surface, 'red', (screen_width/2 - 98, screen_height/2 - 68, 195, 45), 3)
        blit_text_shadow(f'P{self.id_player + 1} - {self.atual_player.name}', 'red', (screen_width/2, screen_height/2 - 42), self.font)

    def draw_trade_card(self):
        pygame.draw.rect(self.display_surface, 'gray', (screen_width/2 - 200, screen_height/2 - 150, 400, 300))
        pygame.draw.rect(self.display_surface, 'black', (screen_width/2 - 200, screen_height/2 - 150, 400, 300), 3)
        pygame.draw.rect(self.display_surface, 'green', (screen_width/2 - 198, screen_height/2 - 148, 395, 295), 3)
        # inside
        pygame.draw.rect(self.display_surface, 'black', (screen_width/2 - 180, screen_height/2 - 115, 360, 250), 3)
        pygame.draw.rect(self.display_surface, 'red', (screen_width/2 - 177, screen_height/2 - 112, 354, 244), 3)
        blit_text_shadow(f'Trade  Card', 'red', (screen_width/2 - 5, screen_height/2 - 127), self.font)
        # collisions
        for i in range(len(self.players)):
            if i != self.id_player:
                self.display_surface.blit(self.trade_collisions[i], self.trade_coll_rect[i])
                pygame.draw.rect(self.display_surface, 'red', (self.trade_coll_pos[i][0], self.trade_coll_pos[i][1], 80, 50), 3)
                blit_text_shadow(f'P{i+1}: {self.players[i].get_qnt_cards()}', 'red', (self.trade_coll_pos[i][0] + 42, self.trade_coll_pos[i][1] + 25), self.font)
        self.display_surface.blit(self.trade_cancel_coll, self.trade_cancel_rect)
        pygame.draw.rect(self.display_surface, 'red', (screen_width/2 - 65, screen_height/2 + 75, 120, 50), 3)
        blit_text_shadow(f'CANCEL', 'red', (screen_width/2 - 5, screen_height/2 + 102), self.font)

    def draw_plys_behind(self):
        # right
        pygame.draw.rect(self.display_surface, 'blue', (screen_width - 60, screen_height/2 - 100, 65, 100))
        pygame.draw.rect(self.display_surface, 'black', (screen_width - 60, screen_height/2 - 100, 65, 100), 3)
        if self.id_player < len(self.players)-1:
            id = (self.id_player + 1) + 1  
            index = id - 1
        else:
            id = 1
            index = 0
        blit_text_shadow(f'P{id}', 'red', (screen_width - 30, screen_height/2 - 80), self.font)
        blit_text_shadow(f'{self.players[index].get_qnt_cards()}', 'red', (screen_width - 30, screen_height/2 - 50), self.font)
        if self.cnt_clockwise:
            self.display_surface.blit(self.next_section_surf, (screen_width - 45, screen_height/2 - 40))
        pygame.draw.rect(self.display_surface, 'black', (screen_width - 44, screen_height/2 - 68, 25, 30), 2)
        # left
        pygame.draw.rect(self.display_surface, 'blue', (-5, screen_height/2 - 100, 65, 100))
        pygame.draw.rect(self.display_surface, 'black', (-5, screen_height/2 - 100, 65, 100), 3)
        if self.id_player > 0:
            id = (self.id_player + 1) - 1  
            index = id - 1
        else:
            id = len(self.players)
            index = (len(self.players)-1)
        blit_text_shadow(f'P{id}', 'red', (25, screen_height/2 - 80), self.font)
        blit_text_shadow(f'{self.players[index].get_qnt_cards()}', 'red', (25, screen_height/2 - 50), self.font)
        if not self.cnt_clockwise:
            self.display_surface.blit(self.prev_section_surf, (5, screen_height/2 - 40))
        pygame.draw.rect(self.display_surface, 'black', (11, screen_height/2 - 68, 25, 30), 2)

    def draw(self):
        self.display_surface.blit(self.background, self.background_rect)
        self.draw_bottom_elements()
        self.draw_table_elements()
        self.draw_plys_behind()
        if self.change_color:
            self.display_surface.blit(self.change_color_surf, self.change_color_rect)
        if self.show_name_timer.run:
            self.draw_atual_player_name()
        if self.trade_card:
            self.draw_trade_card()
    