import pygame as pg
from map import Map
from utils import load_image, Config
from player import Camera
from screens.start import start_screen


def play_screen(screen, level_index, font):
    pg.display.set_caption('Уровень {}'.format(level_index + 1))
    tiles_group = pg.sprite.Group()
    wall_group = pg.sprite.Group()
    finish_group = pg.sprite.Group()
    player_group = pg.sprite.Group()
    
    level_map = Map(level_index)
    level_map.load()
    player, door = level_map.tiles([tiles_group, wall_group], [player_group], [finish_group])
    running = True
    clock = pg.time.Clock()
    camera = Camera()
    played_time = 0
    
    key_up, key_down, key_left, key_right = False, False, False, False

    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_LEFT:
                    key_left = True
                if event.key == pg.K_RIGHT:
                    key_right = True
                if event.key == pg.K_UP:
                    key_up = True
                if event.key == pg.K_DOWN:
                    key_down = True
            if event.type == pg.KEYUP:
                if event.key == pg.K_LEFT:
                    key_left = False
                if event.key == pg.K_RIGHT:
                    key_right = False
                if event.key == pg.K_UP:
                    key_up = False
                if event.key == pg.K_DOWN:
                    key_down = False
        
        if player.doupdate:
            speed1, speed2 = 0, 0
            if key_left and key_right:
                speed1 = 0
            elif key_left:
                speed1 = -9
            elif key_right:
                speed1 = 9
            if key_up:
                speed2 = -11
            player.speed(speed1, speed2)
        elif door.endanim:
            if player.rect.x + player.rect.w // 2 > door.rect.x + door.rect.w // 2:                
                door.activate = False
                player.rect.x -= 1
            else:
                break
        screen.fill([0, 0, 0])
        tiles_group.update(player)
        player_group.update(wall_group)
        camera.update(player, *Config.size)
        if player.doupdate and pg.sprite.spritecollideany(player, finish_group):
            player.doupdate = False
            door.activate = True
            player.door(door)
        for sprite in tiles_group:
            camera.apply(sprite, *Config.size)
        for sprite in player_group:
            camera.apply(sprite, *Config.size)
        tiles_group.draw(screen)
        player_group.draw(screen)
        txt_surface1 = font.render('Прошло: {0:.1f} c'.format(played_time / 1000), True, Config.INPUT_INACTIVE)
        txt_surface2 = font.render('Монет: {}'.format(player.score), True, Config.INPUT_INACTIVE)
        screen.blit(txt_surface1, (0, 0))
        screen.blit(txt_surface2, (0, 50))
        pg.display.flip()
        dtau = clock.tick(Config.FPS)
        if player.doupdate:
            played_time += dtau
    return played_time, player.score
