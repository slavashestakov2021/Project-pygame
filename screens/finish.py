import pygame as pg
from utils import load_image, Config, terminate


def to_n(s, n):
    return s + ' ' * (n - len(s))


def printed(data):
    new_data = []
    for x in data:
        tt = sum(_[0] for _ in data[x])
        ts = sum(_[1] for _ in data[x])
        new_data.append([-ts, -tt, x])
    new_data.sort()
    strs = []
    for x in new_data:
        strs.append(['• ' + x[2], str(-x[0]), '{:.1f}'.format(-x[1] / 1000)])
    return strs


def finish_screen(screen, font, data):
    strs = [["    Имя", "Монет", "Время"]] + printed(data)
    pg.display.set_caption("Slava's Mario")
    clock = pg.time.Clock()
    intro_text = ["    Игра пройдена!", "", "", "", "  Таблица результатов:"]
    fon = pg.transform.scale(load_image('fon.jpg'), Config.size)
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT or event.type == pg.KEYDOWN or event.type == pg.MOUSEBUTTONDOWN:
                return
        screen.blit(fon, (0, 0))
        text_coord = 50
        for line in intro_text:
            string_rendered = font.render(line, 1, pg.Color('black'))
            intro_rect = string_rendered.get_rect()
            text_coord += 10
            intro_rect.top = text_coord
            intro_rect.x = 10
            text_coord += intro_rect.height
            screen.blit(string_rendered, intro_rect)
        text_coord += 20
        xcords = [10, 350, 500]
        for line in strs:
            for i, elem in enumerate(line):
                string_rendered = font.render(elem, 1, pg.Color('black'))
                intro_rect = string_rendered.get_rect()
                intro_rect.top = text_coord
                intro_rect.x = xcords[i]
                screen.blit(string_rendered, intro_rect)
            text_coord += intro_rect.height
        pg.display.flip()
        clock.tick(Config.FPS)
