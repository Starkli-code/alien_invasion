import pygame

from alien import Alien
from ship import Ship
import game_functions as gf
from settings import Settings
from pygame.sprite import Group
from game_stats import Gamestats
from button import Button
from scoreboard import Scoreboard


def run_game():
    pygame.init()

    ai_settings = Settings()
    pygame.display.set_caption("Alien Invasion")
    screen = pygame.display.set_mode(
        (ai_settings.screen_width, ai_settings.screen_height))

    ship = Ship(ai_settings, screen)
    stats = Gamestats(ai_settings)
    button = Button(ai_settings, screen, "Play")
    scoreboard = Scoreboard(ai_settings,screen,stats)
    bullets = Group()
    aliens = Group()

    gf.creat_fleet(ai_settings, screen, aliens)

    # 主循环
    while True:
        screen.fill(ai_settings.bg_color)

        # 监视鼠标键盘
        gf.check_events(ai_settings, stats, button, screen, ship, aliens, bullets,scoreboard)
        if stats.game_stats:
            # 更新子弹
            gf.update_bullets(ai_settings, screen, stats, scoreboard, ship, bullets, aliens)

            # 更新外星人
            gf.update_aliens(ai_settings, stats, screen, aliens, ship, bullets, scoreboard)

            ship.update()
        # 更新屏幕
        gf.update_screen(ai_settings, stats, screen, ship, bullets, aliens, button, scoreboard)


run_game()
