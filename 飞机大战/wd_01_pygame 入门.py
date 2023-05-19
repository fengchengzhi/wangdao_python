import pygame

pygame.init()
hero_rect = pygame.Rect(150, 500, 102, 126)
print(hero_rect.size)
screen = pygame.display.set_mode((480, 700))
bg = pygame.image.load('./images/background.png')
screen.blit(bg, (0, 0))
hero = pygame.image.load('./images/me1.png')
screen.blit(hero, (200, 500))
clock = pygame.time.Clock()
while True:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    hero_rect.y -= 1
    screen.blit(bg, (0, 0))
    screen.blit(hero, hero_rect)
    pygame.display.update()
    if hero_rect.top <= 0:
        hero_rect.y = 700


pygame.quit()
