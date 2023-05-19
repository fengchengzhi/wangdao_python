import pygame
import random

SCREEN_RECT = pygame.Rect(0, 0, 480, 700)
FRAME_PER_SEC = 60
CREATE_ENEMY_EVENT = pygame.USEREVENT
HERO_FIRE_EVENT = pygame.USEREVENT + 1


class GameSprite(pygame.sprite.Sprite):
    def __init__(self, image_name, speed=1):
        super().__init__()
        self.image = pygame.image.load(image_name)
        self.speed = speed
        self.rect = self.image.get_rect()

    def update(self, *args):
        self.rect.y += self.speed


class Background(GameSprite):
    def __init__(self, is_alt=False):
        super().__init__('./images/background.png')
        if is_alt:
            self.rect.y = -self.rect.height

    def update(self):
        super().update()
        if self.rect.y >= self.rect.height:
            self.rect.y = -self.rect.height


class Enemy(GameSprite):
    def __init__(self):
        super().__init__('./images/enemy1.png')
        self.rect.y = -self.rect.height
        self.rect.x = random.randint(0, SCREEN_RECT.width - self.rect.width)
        self.speed = random.randint(1, 3)

    def update(self):
        super().update()
        if self.rect.y >= SCREEN_RECT.height:
            self.kill()


class Bullet(GameSprite):
    def __init__(self):
        super().__init__('./images/bullet1.png', -5)

    def update(self):
        super().update()
        if self.rect.bottom < 0:
            self.kill()


class Hero(GameSprite):
    def __init__(self):
        super().__init__('./images/me1.png')
        self.rect.x = 120
        self.rect.bottom = SCREEN_RECT.bottom - 50
        self.speed = 0
        self.bullets = pygame.sprite.Group()
        self.speed_ud = 0

    def update(self):
        self.rect.x += self.speed
        self.rect.y += self.speed_ud

    def fire(self):
        bullet = Bullet()
        bullet.rect.y = self.rect.y - 10
        bullet.rect.centerx = self.rect.centerx
        self.bullets.add(bullet)
