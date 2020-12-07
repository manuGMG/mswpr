import time, sys, os, json
import pygame
from board import Board
pygame.init()

tiles = []
clock = pygame.time.Clock()
time_delay = 100
timer_event = pygame.USEREVENT+1
pygame.time.set_timer(timer_event, time_delay)

class Tile:
    def __init__(self, x, y, size, value, board):
        self.x = x
        self.y = y
        self.size = size
        self.value = value
        self.board = board
        self.bg_color = hidden_color
        self.hidden = True
        self.marked = False
    
    def draw(self, screen, font):
        if self.hidden == True:
            if self.marked == False:
                pygame.draw.rect(screen, self.bg_color, (self.x, self.y, self.size, self.size))
                pygame.draw.rect(screen, border_color, (self.x, self.y, self.size, self.size), 1)
            else:
                pygame.draw.rect(screen, border_color, (self.x, self.y, self.size, self.size))
                pygame.draw.rect(screen, border_color, (self.x, self.y, self.size, self.size), 1)
                value = font.render('!', False, flag_text_color)
                screen.blit(value, (self.x+self.size/4, self.y+self.size/4))
        else:
                if self.value == -1:
                    pygame.draw.rect(screen, flag_color, (self.x, self.y, self.size, self.size))
                    pygame.draw.rect(screen, flag_color, (self.x, self.y, self.size, self.size), 1)
                    value = font.render('!', False, flag_text_color)
                    screen.blit(value, (self.x+self.size/4, self.y+self.size/4))
                else:
                    pygame.draw.rect(screen, bg_color, (self.x, self.y, self.size, self.size))
                    pygame.draw.rect(screen, border_color, (self.x, self.y, self.size, self.size), 1)
                    if self.value == 1:
                        value = font.render(str(self.value), False, tile_one_color)
                        screen.blit(value, (self.x+self.size/4, self.y+self.size/4))
                    elif self.value == 2:
                        value = font.render(str(self.value), False, tile_two_color)
                        screen.blit(value, (self.x+self.size/4, self.y+self.size/4))
                    elif self.value >= 3:
                        value = font.render(str(self.value), False, tile_three_color)
                        screen.blit(value, (self.x+self.size/4, self.y+self.size/4))

    def is_over(self, pos):
        if pos[0] > self.x and pos[0] < self.x + self.size:
            if pos[1] > self.y and pos[1] < self.y + self.size:
                return True
        self.bg_color = hidden_color

    def get_adjacent_tiles(self):
        adjacent_tiles = []
        x = int(self.x/self.size)
        y = int(self.y/self.size)
        bounds = [[x-1, y-1], [x, y-1], [x+1, y-1], [x+1, y], [x+1, y+1], [x, y+1], [x-1, y+1], [x-1, y]]
        for tile in tiles:
            if tile.hidden == True:
                for i in range(8):
                    if tile.x/self.size == bounds[i][0] and tile.y/self.size == bounds[i][1]:
                        if tile.value != -1:
                            adjacent_tiles.append([tile.x, tile.y])
        return adjacent_tiles

    def reveal(self, extend = False):
        if self.hidden == True or extend == True:
            if self.value != -1:
                self.hidden = False
                if self.value == 0:
                    adjacent_tiles = self.get_adjacent_tiles()
                    for tile in tiles:
                        for pos in adjacent_tiles:
                            if pos[0] == tile.x and pos[1] == tile.y:
                                tile.hidden = False
                                if tile.value == 0:
                                    tile.reveal(extend=True)
            else:
                self.hidden = False
                return False
        return True
        
    def mark(self):
        self.marked = True if self.marked == False else False

class Game: 
    '''
    Launch mswpr
    '''
    def __init__(self, size, rows, cols, bombs):
        # Vars
        self.screen = pygame.display.set_mode((size*rows, size*(cols+1)), pygame.DOUBLEBUF)
        self.size = size
        self.rows = rows
        self.cols = cols
        self.bombs = bombs
        # Import font
        self.font = pygame.font.Font(os.path.join(os.path.curdir, 'res', 'VCR_OSD_MONO.ttf'), round(size/2))
        self.font_big = pygame.font.Font(os.path.join(os.path.curdir, 'res', 'VCR_OSD_MONO.ttf'), round(size))
        # Main loop
        self.playing = True
        self.time = 0
        # Set icon
        pygame.display.set_icon(pygame.image.load(os.path.join(os.path.curdir, 'res', '64x64-ico.png')))
        self.mainloop()

    def generate(self):
        self.time = 0
        tiles.clear()
        # Generate MS Board
        self.board = Board(self.rows, self.cols, self.bombs).generate()
        # Generate tiles
        x = 0
        tx = 0
        for rows in self.board:
            y = 0
            for val in rows:
                if tx == self.cols:
                    x += 1
                    tx = 0
                tiles.append(Tile(x*self.size, y*self.size, self.size, val, self.board))
                y += 1
                tx += 1

    def mainloop(self):
        self.generate()
        while True:
            clock.tick(60)
            self.check_events()
            self.render()
            if self.playing == True:
                pygame.display.set_caption('Mswpr - Playing..')
            else:
                pygame.display.set_caption('Mswpr - Press R to Restart')
            pygame.display.update()

    def check_events(self):
        for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    sys.exit()
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    self.playing = True
                    self.generate()
                elif event.type == pygame.MOUSEBUTTONUP and self.playing == True:
                    if event.button == 1:
                        for tile in tiles:
                            if tile.is_over(pygame.mouse.get_pos()):
                                self.playing = True if tile.reveal() == True else False
                    elif event.button == 3:
                        for tile in tiles:
                            if tile.is_over(pygame.mouse.get_pos()):
                                tile.mark()
                elif event.type == timer_event and self.playing == True:
                    self.time += .1
        pass

        visible_tile_count = 0
        for tile in tiles:
            if tile.is_over(pygame.mouse.get_pos()):
                tile.bg_color = hover_color
            if tile.hidden == False:
                visible_tile_count += 1
        
        if visible_tile_count == ((self.rows*self.cols)-self.bombs):
            self.playing = False

    def render(self):
        for tile in tiles:
            tile.draw(self.screen, self.font)

        text = self.font_big.render(str(round(self.time, 2)) if self.time < 60 else time.strftime('%Mm,%Ss', time.gmtime(self.time)), False, text_color)
        surface = pygame.Surface((self.size*self.rows, self.size))
        surface.fill(bg_color)
        surface.blit(text, (0, -2))
        self.screen.blit(surface, (0, (self.size*self.cols+1)))
        pass

if __name__ == '__main__':
    if len(sys.argv) == 6:
        with open(os.path.join(os.path.curdir, 'themes', sys.argv[1]), 'r') as f:
            json_theme = json.loads(f.read())

            # Colors
            bg_color = (json_theme['bg_color'][0], json_theme['bg_color'][1], json_theme['bg_color'][2])
            border_color = (json_theme['border_color'][0], json_theme['border_color'][1], json_theme['border_color'][2])
            hidden_color = (json_theme['hidden_color'][0], json_theme['hidden_color'][1], json_theme['hidden_color'][2])
            hover_color = (json_theme['hover_color'][0], json_theme['hover_color'][1], json_theme['hover_color'][2])
            text_color = (json_theme['text_color'][0], json_theme['text_color'][1], json_theme['text_color'][2])
            tile_one_color = (json_theme['tile_one_color'][0], json_theme['tile_one_color'][1], json_theme['tile_one_color'][2])
            tile_two_color = (json_theme['tile_two_color'][0], json_theme['tile_two_color'][1], json_theme['tile_two_color'][2])
            tile_three_color = (json_theme['tile_three_color'][0], json_theme['tile_three_color'][1], json_theme['tile_three_color'][2])
            flag_color = (json_theme['flag_color'][0], json_theme['flag_color'][1], json_theme['flag_color'][2])
            flag_text_color = (json_theme['flag_text_color'][0], json_theme['flag_text_color'][1], json_theme['flag_text_color'][2])

        Game(size=int(sys.argv[2]), 
            rows=int(sys.argv[3]), 
            cols=int(sys.argv[4]), 
            bombs=int(sys.argv[5]))
    else:
        print('Mswpr')
        print('Usage: game.py [theme] [block size (px)] [rows] [columns] [bombs]')