class Settings:

    def __init__(self):
        # 游戏背景
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)

        # 飞船

        self.ship_limit = 3

        # 子弹

        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = 60, 60, 60
        self.bullets_allowed = 10

        # 外星人

        self.fleet_drop_factor = 50

        # 以什么样的速度加快游戏速度
        self.speedup_scale = 1.2
        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        self.ship_speed_factor = 1.5
        self.bullet_speed_factor = 3
        self.alien_speed_factor = 1
        self.alien_score = 50

        self.fleet_direction = 1  # 1：向右 -1：向左

    def increase_speed(self):
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        self.alien_score = int(self.speedup_scale * self.alien_score)