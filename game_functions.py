import sys
import pygame
from random import randint
from objects_and_classes import Dinosaur, Cactus, Decoration


def  get_image():
    """рандомное изображение кактуса"""

    images = ('images/cactus1.bmp', 'images/cactus2.bmp', 'images/cactus3.bmp',
              'images/cactus4.bmp')
    image = images[randint(0, 3)]
    return image


def clean_screen(groupa, groupb=None):
    """очищает экран по двум аргументам"""

    if groupa is not None:
        for element in groupa:
            groupa.remove_internal(element)

    if groupb is not None:
        for element in groupb:
            groupb.remove_internal(element)


def check_position(screen, settings, stats, dinosaur, cactuses, best_score_board):
    """функция проверки столкновения динозавра с другим игровым объектом"""

    for cactus in cactuses:
        # если координаты динозавра совпадают с координатами кактуса, то динозавр умирает и происходит выход из игры
        if dinosaur.object_rect.right > cactus.object_rect.left and \
                dinosaur.object_rect.centerx < cactus.object_rect.right and \
                dinosaur.object_rect.bottom > cactus.object_rect.top:
            stats.game_active = False
            update_best_score_board(stats, best_score_board)

        # если правая граница кактуса выходит за пределы экрана, то оно меняет свои координаты на стартовые
        if cactus.object_rect.right < 0:
            cactuses.remove_internal(cactus)
            stats.score += 1
            # проверка увелечения скорости
            check_difficult(stats, settings)
    # если кактусов 0, то создаеся новый
    if len(cactuses) == 0:
        cactus = Cactus(get_image(), screen, settings)
        cactuses.add_internal(cactus)


def bg_check_collision(bg_objects, new_object):
    """проверка 'столкновений' объектов фона """

    for bg_object in bg_objects:
        # если левый край нового объекта находится ближе к началу экрана,
        # чем правый край какого-либо из объектов того же слоя,
        # то координаты нового объекта переносятся на 50 пикселей вправо
        if new_object.object_rect.left <= bg_object.object_rect.right and \
                new_object.layer == bg_object.layer:
            new_object.offset()


def bg_objects_check(screen, settings, bg_objects):
    """контроль объектов фона (их добавление, удаление и проч.)"""

    # если объектов на экране меньше 6, то создается еще один
    if len(bg_objects) < 7:
        layer = randint(0, 4)
        # если выпал 3 слой, то в качестве картинки выступает облако
        if layer > 1:
            new_object = Decoration('images/сloud.bmp', screen, settings, layer)
        # иначе - какой-нибудь кактус
        else:
            new_object = Decoration(get_image(), screen, settings, layer)
        # создание этого объекта, его проверка и добавление его в группу
        bg_check_collision(bg_objects, new_object)
        bg_objects.add_internal(new_object)

    # если объект вышел за пределы экрана, то он удаляется
    for bg_object in bg_objects:
        if bg_object.x < -30:
            bg_objects.remove_internal(bg_object)


def jump(dinosaur):
    """функция прыжка динозавра"""

    # если динозавр на земле, то прыжок возможен
    if dinosaur.dino_y >= dinosaur.screen_floor:
        dinosaur.is_jumping = True


def check_difficult(stats, settings):
    """увеличивает скорость объектов в зависимости от набранных очков"""

    if stats.score % 10 == 0 and stats.score != 0:
        settings.speedup_objects()


def update_scoreboard(stats, scoreboard):
    """обновляет и выводит статистику"""

    scoreboard.message = 'SCORE:{}'.format(stats.score)
    scoreboard.update_message()
    scoreboard.draw()


def update_best_score_board(stats, best_score_board):
    """обновляет лучший счет"""

    stats.best_score_load()
    best_score_board.message = 'HIGH SCORE:{}'.format(stats.best_score)
    best_score_board.update_message()
    stats.best_score_save()


def start_game(settings, stats, dinosaur, cactuses, bg_objects):
    """начинает игру, очистив перед этим экран"""

    # начинается только обновление динозавра
    # остальные объекты начнут обновлятся только когда флаг game_starting перейдет в активное состояние
    stats.game_active = True
    stats.reset_stats()
    settings.dynamic_settings()
    clean_screen(cactuses, bg_objects)
    dinosaur.start_position()


def check_event(settings, stats, dinosaur, cactuses, bg_objects):
    """обработка нажатий клавиш"""

    # отлавливание действие юзера
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        elif event.type == pygame.KEYDOWN:
            # если нажат пробел, то динозавр прыгает и стрелка вверх
            if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                jump(dinosaur)

            elif event.key == pygame.K_DOWN:
                dinosaur.jump_speed_changing_change_flag = True

            # при старте игры динозавр делает один прыжок, после чего начинается сама игра
            elif event.key == pygame.K_p:
                start_game(settings, stats, dinosaur, cactuses, bg_objects)
                if not stats.game_starting:
                    jump(dinosaur)

        elif event.type == pygame.KEYUP:
            # пока клавиша вниз не отжата, происходит ускоренное падение
            if event.key == pygame.K_DOWN:
                dinosaur.jump_speed_changing_change_flag = False


def draw_screen(screen, settings, stats, dinosaur, cactuses, bg_objects,
                play_button, scoreboard, best_score_board):
    """вывод изображения на экран"""

    # делаем фон нужного цвета
    screen.fill(settings.bg_color)

    # отрисовываем игровые объекты
    for cactus in cactuses:
        cactus.draw()
    for bg_object in bg_objects:
        bg_object.draw()
    dinosaur.draw()

    # обновление счетчика очков
    update_scoreboard(stats, scoreboard)
    # отрисовка кнопки play поверх других элементов и вывод лучшего счета
    if not stats.game_active:
        play_button.draw()
        best_score_board.draw()

    # если динозавр приземлился в первый раз, то запускаются кактусы и объекты фона
    if dinosaur.is_landed:
        stats.game_starting = True

    pygame.display.flip()
