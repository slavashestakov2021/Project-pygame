import pygame as pg
from utils import load_image, Config


class Tile(pg.sprite.Sprite):    
    images = {}
    
    @staticmethod
    def tile_images(name):
        if name not in Tile.images:
            Tile.images[name] = load_image(name + '.png')
        return Tile.images[name]
    
    def __init__(self, tile_type, pos_x, pos_y, groups):
        super().__init__(*groups)
        self.image = Tile.tile_images(tile_type)
        self.rect = self.image.get_rect().move(Config.tile_width * pos_x, Config.tile_height * pos_y)


class Door(pg.sprite.Sprite):
    frames = None
    
    @staticmethod
    def load_image(name):
        if not Door.frames:
            image = load_image(name + '.png')
            Door.frames = []
            for j in range(3):
                for i in range(4):
                    frame_location = (Config.tile_width * j, Config.tile_height * i)
                    Door.frames.append(image.subsurface(pg.Rect(frame_location, (Config.tile_width, Config.tile_height))))
    
    def __init__(self, tile_type, pos_x, pos_y, groups):
        super().__init__(*groups)
        Door.load_image(tile_type)
        self.image = Door.frames[0]
        self.rect = self.image.get_rect().move(Config.tile_width * pos_x, Config.tile_height * pos_y)
        self.state, self.activate, self.cadr = 0, False, 0
        self.endanim = False
    
    def update(self, *args):
        if self.activate:
            self.cadr += 1
            if self.cadr % 30 == 0:
                self.state = (self.state + 1) % 4
                self.image = Door.frames[self.state]
                if not self.state:
                    self.endanim = True
                    self.state = 3
                    self.image = Door.frames[3]


class Coin(pg.sprite.Sprite):    
    images = {}
    
    @staticmethod
    def tile_images(name):
        if name not in Coin.images:
            Coin.images[name] = load_image(name + '.png')
        return Coin.images[name]
    
    def __init__(self, tile_type, pos_x, pos_y, groups):
        super().__init__(*groups)
        self.image = Coin.tile_images(tile_type)
        self.score = [1, 5, 10, 50, 100, 500][int(tile_type[4:]) - 1]
        self.rect = self.image.get_rect().move(Config.tile_width * pos_x, Config.tile_height * pos_y)
        self.drawing = True
    
    def update(self, player):
        if self.drawing and self.rect.colliderect(player.rect):
            self.drawing = False
            player.score += self.score
            self.image = Tile.tile_images('sky')
