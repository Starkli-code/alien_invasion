import sys
from time import sleep

import pygame
from bullet import Bullet
from alien import Alien


# 监听事件（鼠标/键盘）
def check_keydown_events(event, ai_settings, screen, ship, bullets):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        if len(bullets) < ai_settings.bullets_allowed:
            new_bullet = Bullet(ai_settings, screen, ship)
            bullets.add(new_bullet)


def check_keyup_events(event, ai_settings, screen, ship, bullets):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False


def check_events(ai_settings, stats, button, screen, ship, aliens, bullets, scoreboard):
    for event in pygame.event.get():
        # 控制游戏开关
        if event.type == pygame.QUIT:
            sys.exit()
        # 控制子弹
        elif event.type == pygame.K_SPACE:
            check_keydown_events(event, ai_settings, screen, ship, bullets)

        # 控制飞船左右移动
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets)

        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ai_settings, screen, ship, bullets)
        # 控制游戏开始
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, button, ship, aliens, bullets, mouse_x, mouse_y, scoreboard)


def check_play_button(ai_settings, screen, stats, button, ship, aliens, bullets, mouse_x, mouse_y, scoreboard):
    button_clicked = button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_stats:
        pygame.mouse.set_visible(False)
        stats.reset_stats()
        stats.game_stats = True
        ai_settings.initialize_dynamic_settings()

        aliens.empty()
        bullets.empty()

        scoreboard.prep_level()
        scoreboard.prep_score()
        scoreboard.prep_high_score()
        scoreboard.prep_ship()

        creat_fleet(ai_settings, screen, aliens)
        ship.center_ship()


# 更新屏幕
def update_screen(ai_settings, stats, screen, ship, bullets, aliens, button, scoreboard):
    screen.fill(ai_settings.bg_color)
    scoreboard.show_score()

    for bullet in bullets:
        bullet.draw_bullet()

    aliens.draw(screen)
    ship.blitme()

    if not stats.game_stats:
        button.draw()

    pygame.display.flip()


# 更新子弹
def update_bullets(ai_settings, screen, stats, scoreboard, ship, bullets, aliens):
    bullets.update()

    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    # collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)
    check_alien_destroy(ai_settings, screen, stats, scoreboard, ship, bullets, aliens)
    if len(aliens) == 0:
        bullets.empty()
        creat_fleet(ai_settings, screen, aliens)
        ai_settings.increase_speed()

        stats.level += 1
        scoreboard.prep_level()


# 外星人相关操作
def get_number_aliens_x(ai_settings, alien_width):
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x


def creat_alien(ai_settings, screen, aliens, alien_number):
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    aliens.add(alien)


def creat_fleet(ai_settings, screen, aliens):
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)

    for alien_number in range(number_aliens_x):
        creat_alien(ai_settings, screen, aliens, alien_number)


def update_aliens(ai_settings, stats, screen, aliens, ship, bullets, scoreboard):
    check_fleet_edges(ai_settings, aliens)
    aliens.update()

    check_fleet_bottom(ai_settings, stats, screen, aliens, ship, bullets, scoreboard)

    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, stats, screen, aliens, ship, bullets, scoreboard)
    # for alien in aliens:
    #     if alien.check_alien_edge():
    #         change_alien_direction(ai_settings, alien)
    #     else:
    #         alien.update()


def check_fleet_edges(ai_settings, aliens):
    for alien in aliens:
        if alien.check_alien_edge():
            change_fleet_direction(ai_settings, aliens)
            break


def check_fleet_bottom(ai_settings, stats, screen, aliens, ship, bullets, scoreboard):
    screen_rect = screen.get_rect()
    for alien in aliens:
        if alien.rect.bottom >= screen_rect.bottom:
            ship_hit(ai_settings, stats, screen, aliens, ship, bullets, scoreboard)
            break


# def change_alien_direction(ai_settings, alien):
#     alien.rect.y += ai_settings.fleet_drop_factor
#     ai_settings.fleet_direction *= -1

def change_fleet_direction(ai_settings, aliens):
    for alien in aliens:
        alien.rect.y += ai_settings.fleet_drop_factor
    ai_settings.fleet_direction *= -1


def check_alien_destroy(ai_settings, screen, stats, scoreboard, ship, bullets, aliens):
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)

    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_score * len(aliens)
            scoreboard.prep_score()
        check_high_score(stats, scoreboard)


# 飞船毁灭
def ship_hit(ai_settings, stats, screen, aliens, ship, bullets, scoreboard):
    stats.ships_left -= 1
    if stats.ships_left > 0:
        aliens.empty()
        bullets.empty()

        creat_fleet(ai_settings, screen, aliens)
        ship.center_ship()

        scoreboard.prep_ship()

        sleep(1)
    else:
        stats.game_stats = False
        pygame.mouse.set_visible(True)


# 记分
def check_high_score(stats, scoreboard):
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        scoreboard.prep_high_score()
