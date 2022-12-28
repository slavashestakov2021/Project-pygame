import pygame as pg
from utils import load_image, Config, Segment, intersect, segments


class Player(pg.sprite.Sprite):
    def __init__(self, pos_x, pos_y, groups):
        super().__init__(*groups)
        self.image = load_image('player.png')
        self.rect = self.image.get_rect().move(Config.tile_width * pos_x + 15, Config.tile_height * pos_y + 5)
        self.vx, self.vy = 0, 0
        self.onground = False
        self.doupdate = True
        self.score = 0

    def movey(self, dy):
        if dy < 0:
            self.vy = 0
        self.rect.y += dy
    
    def movex(self, dx, last_speed):
        self.vx = 0
        self.rect.x += dx
    
    def speed(self, vx, vy):
        self.vx = vx
        if self.onground:
            self.vy = vy
            self.onground = False
    
    def door(self, door):
        door = door.rect
        self.rect.y = door.y + door.h - self.rect.h
        self.rect.x = door.x + door.w
    
    def update(self, map_group):
        if not self.doupdate:
            return
        self.rect.x += self.vx
        speedx = self.vx
        moving = (self.vx != 0)
        if self.vx > 0:
            self.vx -= 1
        if self.vx < 0:
            self.vx += 1
        if not self.onground:
            self.vy += 1
            self.rect.y += self.vy
            moving = True
        else:
            self.vy = 0
        self.rect.y -= 1
        
        self.onground = False if moving else self.onground
        px, py = segments(self)
        for tile in map_group:
            tx, ty = segments(tile)
            per = intersect(px, tx)
            iy = intersect(py, ty)
            if per and iy:
                ln = per[1] - per[0]
                lny = iy[1] - iy[0]
                if lny > 1:
                    if per[0] == px.x1:
                        self.movex(ln, lny)
                    if per[1] == px.x2:
                        self.movex(-ln, lny)
                    px, py = segments(self)
        
        for tile in map_group:
            tx, ty = segments(tile)
            per = intersect(py, ty)
            if per and intersect(px, tx):
                ln = per[1] - per[0]
                if per[0] == py.x1:
                    self.movey(ln)
                    self.vy = 0
                if per[1] == py.x2:
                    self.movey(-ln)
                    self.onground = True
                px, py = segments(self)


class Camera:
    def __init__(self):
        self.dx = 0
        self.dy = 0

    def apply(self, obj, W, H):
        obj.rect.x += self.dx
        obj.rect.y += self.dy
    
    def update(self, target, width, height):
        self.dx = -(target.rect.x + target.rect.w // 2 - width // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - height // 2)
