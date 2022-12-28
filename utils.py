import pygame as pg
import sys
import pickle


def load_image(name):
    return pg.image.load('images/' + name)


def terminate():
    pg.quit()
    sys.exit()


class Config:
    FPS = 50
    BORDER = 10
    tile_width = tile_height = 50
    size = width, height = 15 * tile_width, 15 * tile_height
    INPUT_INACTIVE = pg.Color('green2')
    INPUT_ACTIVE = pg.Color('red2')


class Segment:
    def __init__(self, s, d):
        self.x1, self.x2 = s, s + d


def intersect(s1, s2):
    start = max(s1.x1, s2.x1)
    finish = min(s1.x2, s2.x2)
    return [start, finish] if start < finish else None


def segments(obj):
    rect = obj.rect
    return Segment(rect.x, rect.w), Segment(rect.y, rect.h)


def read_data():
    try:
        with open('data.dat', 'rb') as file:
            data = pickle.load(file)
        return data
    except Exception:
        return {}


def write_data(data):
    with open('data.dat', 'wb') as file:
        pickle.dump(data, file)
