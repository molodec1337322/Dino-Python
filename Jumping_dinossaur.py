import pygame
from pygame.sprite import Group
from time import sleep
import game_functions as gf
from settings import Settings
from objects_and_classes import Dinosaur, Cactus, Text, Stats


def init_main():
    """инициализация главного окна"""

    pygame.init()

    # импорт настроек и их применение
    g_settings = Settings()
    screen = pygame.display.set_mode((g_settings.screen_width, g_settings.screen_height))
    pygame.display.set_caption('Jumping dinosaur (like in famous Google Chrome game!)')

    # создание объектов
    stats = Stats(g_settings, 0, 'Records.txt')
    play_button = Text(g_settings, screen, 'PLAY')
    scoreboard = Text(g_settings, screen, 'SCORE:{}'.format(stats.score), 'Right')
    best_score_board = Text(g_settings, screen, 'HIGH SCORE:{}'.format(stats.best_score), 'Left')
    dinosaur = Dinosaur(screen, g_settings)
    cactuses = Group()
    bg_objects = Group()
    # основной цикл программы
    while True:
        gf.check_event(g_settings, stats, dinosaur, cactuses, bg_objects)

        if stats.game_active:
            dinosaur.update()
            if stats.game_starting:
                cactuses.update()
                bg_objects.update()
                # проверка положения кактусов и динозавра
                gf.check_position(screen, g_settings, stats, dinosaur, cactuses, best_score_board)
                # проверка положения объектов на заднем фоне
                gf.bg_objects_check(screen, g_settings, bg_objects)

        # отрисовка экрана
        gf.draw_screen(screen, g_settings, stats, dinosaur, cactuses, bg_objects,
                       play_button, scoreboard, best_score_board)

        # задержка нужна для того, чтобы скорость перемещения объектов на всех компьютерах была одинаковой
        sleep(0.005)


if __name__ == '__main__':
    init_main()