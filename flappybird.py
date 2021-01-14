import sys

import pygame
from Box2D.b2 import world, polygonShape, circleShape, staticBody, dynamicBody
from Box2D import b2Vec2
import random
import os


def load_image(name, color_key=None):
    fullname = os.path.join(name)
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


def my_draw_polygon(polygon, body, fixture):
    pass


def my_draw_circle(circle, body, fixture):
    pass


class Bird(pygame.sprite.Sprite):
    def __init__(self, all_sprites):
        super().__init__(all_sprites)
        self.body = world.CreateDynamicBody(position=(5, 20))
        circle = self.body.CreateCircleFixture(radius=1, density=1, friction=0, categoryBits=3, maskBits=2)
        self.radius = 20
        # self.image = pygame.Surface((62, 48), pygame.SRCALPHA, 32)
        self.sprites = [load_image("bird1.png", -1), load_image("bird2.png", -1),
                        load_image("bird3.png", -1), load_image("bird2.png", -1)]
        self.an = 0
        self.image = self.sprites[self.an]
        # pygame.draw.circle(self.image, pygame.Color("red"), (20, 20), 20)
        self.rect = pygame.Rect(80, 380, 61, 44)
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.rect.x = self.body.position[0] * PPM - 20
        self.rect.y = SCREEN_HEIGHT - self.body.position[1] * PPM - 20

    def jump(self):
        self.body.linearVelocity = b2Vec2(0, 0)
        self.body.ApplyLinearImpulse(b2Vec2(0, 40), self.body.position, True)

    def animation(self):
        self.an += 1
        self.an %= 4
        self.image = self.sprites[self.an]


class Post(pygame.sprite.Sprite):
    def __init__(self, all_sprites, y):
        super().__init__(all_sprites)
        self.y = y
        self.post = world.CreateDynamicBody(position=(33, 40), shapes=polygonShape(box=(3, y)),
                                            linearVelocity=(-5, 0), gravityScale=0)
        # self.image = pygame.Surface((60, y * PPM), pygame.SRCALPHA, 32)
        # pygame.draw.rect(self.image, pygame.Color(0, 255, 0), (0, 0, 60, y * PPM))
        self.image = load_image("postdown.png", -1).subsurface(pygame.Rect(0, 800 - y * PPM, 60, y * PPM))
        self.image.set_colorkey("BLACK")
        self.rect = pygame.Rect(630, 0, 60, y * PPM)
        self.mask = pygame.mask.from_surface(self.image)
        self.wascount = False

    def update(self):
        global score
        self.rect.x = self.post.position[0] * PPM - 60
        if self.rect.x < -60:
            self.kill()
        if self.rect.x <= 100 and not self.wascount:
            bonussaund.play()
            score += 1
            self.wascount = True
        if pygame.sprite.collide_mask(self, bird):
            failsound.play()
            lose()


class BottomPost(pygame.sprite.Sprite):
    def __init__(self, all_sprites, y, post):
        super().__init__(all_sprites)
        self.y = y
        self.post1 = post
        self.post = world.CreateDynamicBody(position=(33, y + 8), shapes=polygonShape(box=(3, 30 - y)),
                                            linearVelocity=(-5, 0), gravityScale=0)
        # self.image = pygame.Surface((60, (30 - y) * PPM), pygame.SRCALPHA, 32)
        # pygame.draw.rect(self.image, pygame.Color(0, 255, 0), (0, 0, 60, (27 - y) * PPM))
        self.image = load_image("postup.png", -1).subsurface(pygame.Rect(0, 0, 60, (27 - y) * PPM))
        self.image.set_colorkey("BLACK")
        self.rect = pygame.Rect(630, (y + 8) * PPM, 60, 789)
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.post.position[0] = self.post1.post.position[0]
        self.rect.x = self.post.position[0] * PPM - 60
        if self.rect.x < -60:
            self.kill()
        if pygame.sprite.collide_mask(self, bird):
            failsound.play()
            lose()


class Ground(pygame.sprite.Sprite):
    def __init__(self, all_sprites):
        super().__init__(all_sprites)
        ground_body = world.CreateStaticBody(position=(0, 0), shapes=polygonShape(box=(30, 5)))
        self.image = load_image("ground.jpg")
        self.rect = pygame.Rect(0, 700, 600, 100)
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        if pygame.sprite.collide_mask(self, bird):
            failsound.play()
            lose()


class Plume(pygame.sprite.Sprite):
    def __init__(self, all_sprites, y, post):
        super().__init__(all_sprites)
        self.post1 = post
        self.post = world.CreateDynamicBody(position=(33, 40 - y - 5), shapes=polygonShape(box=(2, 2)),
                                            linearVelocity=(-5, 0), gravityScale=0)
        self.image = load_image("plume.png", -1)
        self.rect = pygame.Rect(630, (y + 3) * PPM, 40, 40)
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        global score
        self.post.position[0] = self.post1.post.position[0] + 0.5
        self.rect.x = self.post.position[0] * PPM - 60
        if pygame.sprite.collide_mask(self, bird):
            score += 5
            self.kill()


def start():
    global started, running, losed
    print(score)
    for i in postsprites:
        i.kill()
    bird.body.linearVelocity = b2Vec2(0, 0)
    bird.body.position = (5, 20)
    bird.rect.y = 380
    started = False
    losed = True
    running = True


def lose():
    start()


def terminate():
    pygame.quit()
    sys.exit()


def menu():
    global background, background_rect
    TARGET_FPS = 60
    PPM = 20
    TIMESTEP = 1.0 / TARGET_FPS
    clock = pygame.time.Clock()
    SCREEN_WIDTH, SCREEN_HEIGHT = 550, 800
    logo = load_image("logo.png", -1)
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return
        screen.fill("black")
        screen.blit(background, background_rect)
        screen.blit(logo, (0, 0), pygame.Rect(0, 0, 550, 309))
        pygame.display.flip()
        clock.tick(TARGET_FPS)


def get_best_score(n):
    with open("bestscore.txt", "r") as r:
        best = int(r.readline())
    if n > best:
        with open("bestscore.txt", "w") as w:
            w.write(str(n))
        return str(n)
    else:
        return str(best)


if __name__ == '__main__':
    pygame.font.init()
    pygame.display.init()
    pygame.mixer.init()
    TARGET_FPS = 60
    PPM = 20
    TIMESTEP = 1.0 / TARGET_FPS

    SCREEN_WIDTH, SCREEN_HEIGHT = 550, 800

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
    pygame.display.set_caption("flappy bird")
    clock = pygame.time.Clock()

    world = world(gravity=(0, -10))

    polygonShape.draw = my_draw_polygon
    circleShape.draw = my_draw_circle

    birdsprites = pygame.sprite.Group()
    postsprites = pygame.sprite.Group()

    bird = Bird(all_sprites=birdsprites)
    ground = Ground(birdsprites)

    background = load_image("bg2.jpg")
    background_rect = background.get_rect()

    SPAWNPOST = pygame.USEREVENT + 1
    CHANGESPRITE = pygame.USEREVENT + 2
    pygame.time.set_timer(CHANGESPRITE, 100)
    menu()
    bonussaund = pygame.mixer.Sound("bonus.mp3")
    failsound = pygame.mixer.Sound("fail.mp3")

    running = True
    started = False
    losed = False
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if losed:
                    losed = False
                elif started:
                    bird.jump()
                else:
                    started = True
                    score = 0
                    pygame.time.set_timer(SPAWNPOST, 4500)
                    world.gravity = (0, -10)
                    bird.jump()
            if event.type == SPAWNPOST:
                if started:
                    y = random.randint(1, 20)
                    post = Post(all_sprites=postsprites, y=y)
                    BottomPost(all_sprites=postsprites, y=y, post=post)
                    if random.randint(1, 20) == 7:
                        Plume(all_sprites=postsprites, y=y, post=post)
            if event.type == CHANGESPRITE:
                bird.animation()
        screen.fill("black")
        screen.blit(background, background_rect)
        if not started:
            world.gravity = (0, 0)
        for body in world.bodies:
            for fixture in body.fixtures:
                fixture.shape.draw(body, fixture)
        world.Step(TIMESTEP, 10, 10)
        if started:
            font = pygame.font.Font(None, 90)
            text = font.render(str(score), True, (255, 255, 255))
            screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 150 - text.get_height() // 2))
        birdsprites.draw(screen)
        birdsprites.update()
        postsprites.draw(screen)
        postsprites.update()
        if losed:
            font = pygame.font.Font(None, 40)
            pygame.draw.rect(screen, pygame.Color(222, 216, 149), (175, 200, 200, 300))
            pygame.draw.rect(screen, pygame.Color("black"), (175, 200, 200, 300), 5)
            text = font.render("Лучший счет", True, (255, 255, 255))
            bestscore = get_best_score(score)
            screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 240 - text.get_height() // 2))
            text = font.render(str(bestscore), True, (255, 255, 255))
            screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 300 - text.get_height() // 2))
            text = font.render("Текущий счет", True, (255, 255, 255))
            screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 390 - text.get_height() // 2))
            text = font.render(str(score), True, (255, 255, 255))
            screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, 450 - text.get_height() // 2))
        pygame.display.flip()
        clock.tick(TARGET_FPS)
