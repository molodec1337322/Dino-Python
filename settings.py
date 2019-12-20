

class Settings:
    """ настройки и параметры игры """

    def __init__(self):
        # настройки экрана
        self.screen_width = 650
        self.screen_height = 350
        self.bg_color = (255, 255, 255)

        # общие параметры
        self.object_offset = 40

        # параметры динозавра
        self.jump_height = 180.0

        # параметры объектов фона
        self.bg_offset = 50
        self.bg_perspective = (70, 120, 210, 230, 250)

        # ускорение объектов
        self.speedup_factor = 1.05

        # параметры динозавра
        self.dino_speed_factor = 4

    def dynamic_settings(self):
        """ динамические настройки """

        # параметры кактуса
        self.cactus_speed_factor = 4

        # параметры объектов фона
        self.bg_speed_factor = [3.2, 2.4, 1.6, 1.2, 0.8]

    def speedup_objects(self):
        """ увеличивает скорость объектов """

        self.dino_speed_factor *= self.speedup_factor
        self.cactus_speed_factor *= self.speedup_factor
        for factor in self.bg_speed_factor:
            factor *= self.speedup_factor
