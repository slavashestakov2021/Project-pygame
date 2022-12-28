import pygame as pg
from screens import start_screen, play_screen, finish_screen
from utils import Config, read_data, write_data


def main():
    pg.init()
    font = pg.font.Font(None, 32)
    screen = pg.display.set_mode(Config.size)
    user_name = start_screen(screen, font)
    data = read_data()
    if user_name not in data:
        data[user_name] = []
    user = data[user_name]
    while True:
        level = len(user)
        if level == 4:
            break
        info = play_screen(screen, level, font)
        if not info:
            break
        user.append(info)
        data[user_name] = user
        write_data(data)
    finish_screen(screen, font, data)
    pg.quit()


if __name__ == '__main__':
    main()
