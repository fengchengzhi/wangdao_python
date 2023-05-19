import pygame
from plane_sprites import *
import time
from pygame.locals import *


class PlanGame:
    def __init__(self):
        self.screen = pygame.display.set_mode(SCREEN_RECT.size)
        self.clock = pygame.time.Clock()
        self.__create_sprites()
        pygame.time.set_timer(CREATE_ENEMY_EVENT, 1000)
        pygame.time.set_timer(HERO_FIRE_EVENT, 100)

    def __create_sprites(self):
        bg1 = Background()
        bg2 = Background(True)
        self.background_group = pygame.sprite.Group(bg1, bg2)
        self.enemy_group = pygame.sprite.Group()
        self.hero = Hero()
        self.hero_group = pygame.sprite.Group(self.hero)

    def start_game(self):
        while True:
            self.clock.tick(FRAME_PER_SEC)
            self.__event_handler()
            self.__check_collide()
            self.__update_sprites()
            pygame.display.update()

    def __event_handler(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.__game_over(self)
            if event.type == CREATE_ENEMY_EVENT:
                enemy = Enemy()
                self.enemy_group.add(enemy)
            if event.type == HERO_FIRE_EVENT:
                self.hero.fire()
            key_pressed = pygame.key.get_pressed()
            if key_pressed[K_UP]:
                self.hero.speed_ud = -8
            elif key_pressed[K_DOWN]:
                self.hero.speed_ud = 8
            elif key_pressed[K_LEFT]:
                self.hero.speed = -8
            elif key_pressed[K_RIGHT]:
                self.hero.speed = 8
            else:
                self.hero.speed = 0
                self.hero.speed_ud = 0

    def __check_collide(self):
        pygame.sprite.groupcollide(self.hero.bullets, self.enemy_group, True, True)
        enemies = pygame.sprite.spritecollide(self.hero, self.enemy_group, True)
        if len(enemies) > 0:
            self.hero.kill()
            m = "./sound/use_bomb.wav"
            pygame.mixer.music.load(m)
            pygame.mixer.music.play()
            time.sleep(2)
            self.__game_over(self)

    def __update_sprites(self):
        self.background_group.update()
        self.background_group.draw(self.screen)
        self.enemy_group.update()
        self.enemy_group.draw(self.screen)
        self.hero_group.update()
        self.hero_group.draw(self.screen)
        self.hero.bullets.update()
        self.hero.bullets.draw(self.screen)

    @staticmethod
    def __game_over(self):
        pygame.quit()
        exit()


if __name__ == '__main__':
    # 创建游戏对象
    pygame.init()
    game = PlanGame()

    # 启动游戏
    game.start_game()
