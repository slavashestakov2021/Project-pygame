from tile import Tile, Door, Coin
from player import Player
from utils import Config


class Map:
    decode = {' ': 'sky', '#': 'box', '@': 'grass', '1': 'coin1', '2': 'coin2', '3': 'coin3', '4': 'coin4', '5': 'coin5', '6': 'coin6'}

    def __init__(self, level: int):
        self.level_number = level
    
    def load(self):
        filename = "levels/{}.txt".format(self.level_number)
        with open(filename, 'r') as mapFile:
            level = [line.strip() for line in mapFile] 
        self.width = max(map(len, level))
        self.height = len(level)        
        level = list(map(lambda x: x.ljust(self.width, ' '), level))
        self.level = []
        for line in level:
            self.level.append(line[0] * Config.BORDER + line[1:-1] + line[-1] * Config.BORDER)
        for i in range(Config.BORDER - 1):
            self.level.append(self.level[-1])
        self.level.reverse()
        for i in range(Config.BORDER - 1):
            self.level.append(self.level[-1])
        self.level.reverse()
        
    def tiles(self, tile_groups, player_groups, finish_group):
        for y in range(len(self.level)):
            for x in range(len(self.level[y])):
                c = self.level[y][x]
                if c == ' ':
                    Tile(Map.decode[c], x, y, tile_groups[0:1])
                elif c.isdigit():
                    Coin(Map.decode[c], x, y, tile_groups[0:1])
                elif c in Map.decode:
                    Tile(Map.decode[c], x, y, tile_groups)
                if c == 's':
                    Tile(Map.decode[' '], x, y, tile_groups[0:1])
                    player = Player(x, y, player_groups)
                if c == 'f':
                    door = Door('door', x, y, [tile_groups[0], *finish_group])
        return player, door
