import pygame as pg
from utils import load_image, Config, terminate
from inputbox import InputBox


def start_screen(screen, font):
    pg.display.set_caption("Slava's Mario")
    clock = pg.time.Clock()
    intro_text = ["     Платформер", "", "• Прыгайте по полю", "• Собирайте монеты", "• Добирайтесь до финиша", "• Играйте на время"]
    intro_text = [*intro_text, "", "", "", "", "", "   Прогресс игроков запоминается,", "       введите имя игрока:"]
    fon = pg.transform.scale(load_image('fon.jpg'), Config.size)
    input_name = InputBox(50, 500, 210, 32, font)
    while not input_name.inputed:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                terminate()
            input_name.handle_event(event, font)
        input_name.update()
        
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
        input_name.draw(screen)
        pg.display.flip()
        clock.tick(Config.FPS)
    return input_name.inputed
