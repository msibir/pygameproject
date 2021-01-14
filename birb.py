import os
import random
import pygame


def load_image(name, color_key=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname).convert()
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)

    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
    return image


class Bird(pygame.sprite.Sprite):
    def __init__(self, all_sprites):
        super().__init__(all_sprites)
        self.radius = radius
        self.image = pygame.Surface((2 * radius, 2 * radius), pygame.SRCALPHA, 32)
        pygame.draw.circle(self.image, pygame.Color("red"), (radius, radius), radius)
        self.rect = pygame.Rect(500, 500, 2 * radius, 2 * radius)
        self.vy = 0

    def update(self):
        self.vy += g
        self.vy = min(self.vy, maxv)
        self.rect.y = g * fps ** 2 / 2

    def jump(self):
        self.vy = -240


if __name__ == '__main__':
    all_sprites = pygame.sprite.Group()

    radius = 20
    g = 3
    maxv = 240


    size = width, height = 1000, 1000
    screen = pygame.display.set_mode(size)
    fps = 60

    clock = pygame.time.Clock()
    running = True
    bird = Bird(all_sprites)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                bird.jump()
        screen.fill(pygame.Color("white"))
        all_sprites.draw(screen)
        all_sprites.update()
        pygame.display.flip()
        clock.tick(fps)
    pygame.quit()
