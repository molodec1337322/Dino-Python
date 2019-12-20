import pygame
import pygame.font
from random import randint


class GameObjects:
    """ родительский класс вссех игровых объектов """

    def __init__(self, image, screen, settings):
        self.screen = screen
        self.settings = settings

        # загрузка изображения объекта и его применение
        self.image = pygame.image.load(image)
        self.object_rect = self.image.get_rect()
        self.screen_rect = self.screen.get_rect()
        self.screen_floor = float(self.screen_rect.bottom - settings.object_offset)

    def draw(self):
        """отрисовка объекта"""

        self.screen.blit(self.image, self.object_rect)


class Dinosaur(GameObjects):
    """ класс динозавра, которым играет юзер """

    def __init__(self, screen, settings):
        GameObjects.__init__(self, 'images/dinosaur.bmp', screen, settings)

        # спавн динозавра у левого нижнего угла экрана
        self.object_rect.centerx = self.screen_rect.left + settings.object_offset
        self.object_rect.centery = self.screen_rect.bottom - settings.object_offset
        # вещественные координаты динозавра
        self.dino_y = float(self.object_rect.centery)

        # параметры необходимые для прыжка
        self.is_jumping = False
        self.is_landed = False
        self.jump_speed_changing = 0.08
        # флаги необходимые для ускоренного падения
        self.jump_speed_changing_change_flag = False
        self.jump_speed_changing_change = 0.8

    def draw(self):
        """ отрисовка динозавра """

        GameObjects.draw(self)

    def update(self):
        """ прыжок динозавра """

        # когда динозавр прыгает
        if self.is_jumping:
            # если флаг ускоренного падения True, то скоростьь изменяется в 10 раз быстрее
            if self.jump_speed_changing_change_flag:
                self.dino_y -= self.settings.dino_speed_factor
                self.settings.dino_speed_factor -= self.jump_speed_changing_change

            # иначе - изменяется как обычно
            else:
                self.dino_y -= self.settings.dino_speed_factor
                self.settings.dino_speed_factor -= self.jump_speed_changing

        # когда динозавр приземлился, флаг меняется на True
        if self.dino_y >= self.screen_floor:
            # этот флаг нужен только для старта игры
            self.is_landed = True
            # а эти флаги нужны на протяжении всей игры
            # когда координаты динозавра уходят под координаты пола,
            # то флаг прыжка устанавливается в False, скорость становится преженей,
            # а сам динозавр перемещается в стартовые координаты
            self.is_jumping = False
            self.settings.dino_speed_factor = 4
            self.start_position()

        # изменение текущих координат
        self.object_rect.centery = self.dino_y

    def start_position(self):
        """ устанавливает стартовое положение """

        self.is_jumping = False
        self.dino_y = self.screen_floor


class Cactus(GameObjects):
    """ класс кактуса """

    def __init__(self, image, screen, settings):
        GameObjects.__init__(self, image, screen, settings)

        # спавн объекта
        self.start_position = self.screen_rect.right + randint(0, 200)
        self.object_rect.centerx = self.screen_rect.right
        self.object_rect.centery = self.screen_rect.bottom - settings.object_offset
        self.cactus_speed = settings.cactus_speed_factor
        # вещественные координаты катуса
        self.cactus_x = float(self.object_rect.centerx)

    def draw(self):
        """ отрисовка объекта """

        GameObjects.draw(self)

    def update(self):
        """ движение кактусов вправо """

        # изменение текущих координат
        self.cactus_x -= self.settings.cactus_speed_factor

        self.object_rect.centerx = self.cactus_x


class Decoration(GameObjects):
    """ класс задников """

    def __init__(self, image, screen, settings, layer):
        GameObjects.__init__(self, image, screen, settings)

        # слой фона
        self.layer = layer

        # стартовые координаты для объектов фона
        self.object_rect.centerx = self.screen_rect.right + 20
        self.object_rect.centery = self.screen_floor - settings.bg_perspective[self.layer]
        self.x = float(self.object_rect.centerx)

    def draw(self):
        """ отрисовка объектов фона """

        GameObjects.draw(self)

    def update(self):
        """ обновления положения объекта """

        self.x -= self.settings.bg_speed_factor[self.layer]
        self.object_rect.centerx = self.x

    def offset(self):
        """ смещает объект """

        self.x += self.settings.object_offset


class Text:
    """ класс текста """
    def __init__(self, settings, screen, message, side=None):
        super().__init__()

        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.settings = settings
        self.side = side
        self.message = message

        # размеры и свойства надписи
        self.text_color = (180, 180, 180)
        self.bg_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 30)

        # изменение и применение текста
        self.update_message()

    def update_message(self):
        """ создает текст и обновляет """

        self.image = self.font.render(self.message, True, self.text_color, None)
        self.image_rect = self.image.get_rect()
        # если флага стороны нет, то надпись выводится по центру экрана,а иначе в других сторонах
        if self.side is None:
            self.image_rect.center = self.screen_rect.center
        elif self.side == 'Right':
            self.image_rect.top = self.screen_rect.top
            self.image_rect.right = self.screen_rect.right
        elif self.side == 'Left':
            self.image_rect.top = self.screen_rect.top
            self.image_rect.left = self.screen_rect.left

    def draw(self):
        """ отрисовывает надпись """

        self.screen.blit(self.image, self.image_rect)


class Stats:
    """ отслеживание действий """

    def __init__(self, settings, score, filename):
        self.settings = settings
        self.score = score
        self.best_score = 0
        self.game_active = False
        self.game_starting = False
        self.filename = filename

        # сброс и загрузка данных
        self.reset_stats()
        self.best_score_load()

    def reset_stats(self):
        """ инициализарует статистику """

        self.score = 0

    def best_score_load(self):
        """ загружает лучший результат """

        try:
            # загружает лучший результат
            with open(self.filename, 'r') as file:
                self.best_score = file.read()
        # если файл не найден, то создает новый, а лучший счет устанавливается как 0
        except FileNotFoundError:
            with open(self.filename, 'w') as file:
                file.write(str(self.best_score))

    def best_score_save(self):
        """ сохраняет лучший результат """

        # если новый счет лучше старого, то он перезаписывается
        if self.score > int(self.best_score):
            with open(self.filename, 'w') as file:
                file.write(str(self.score))
