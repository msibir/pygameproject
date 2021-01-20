import pygame
from Box2D.b2 import world, polygonShape, circleShape, staticBody, dynamicBody
import os

TARGET_FPS = 60
PPM = 20
TIMESTEP = 1.0 / TARGET_FPS

SCREEN_WIDTH, SCREEN_HEIGHT = 640, 400

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
pygame.display.set_caption("aaaa")
clock = pygame.time.Clock()

world = world(gravity=(0, -10))
all_sprites = pygame.sprite.Group()
ground_body = world.CreateStaticBody(position=(0,0), shapes=polygonShape(box=(50, 1)))

colors = {
    staticBody: (255, 255, 255, 255),
}


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


def my_draw_polygon(polygon, body, fixture):
    vertices = [(body.transform * v) * PPM for v in polygon.vertices]
    vertices = [(v[0], SCREEN_HEIGHT - v[1]) for v in vertices]
    pygame.draw.polygon(screen, colors[body.type], vertices)


polygonShape.draw = my_draw_polygon
radius = 20


class Bird(pygame.sprite.Sprite):
    image = load_image("bird.jpg")
    def __init__(self, *group):
        super().__init__(*group)
        self.radius = radius
        self.rect = self.image.get_rect()
        body = world.CreateDynamicBody(position=(20, 20))
        self.circle = body.CreateCircleFixture(radius=1, density=1, friction=0.3)
        self.rect = pygame.Rect(20, 20, 260, 260)

    def update(self):
        self.rect = self.rect.move(0, self.circle.shape.pos[1])


def my_draw_circle(circle, body, fixture):
    position = body.transform * circle.pos * PPM
    position = (position[0], SCREEN_HEIGHT - position[1])
    circle.rect.draw()


circleShape.draw = my_draw_circle

Bird(all_sprites)
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill("black")
    for body in world.bodies:
        for fixture in body.fixtures:
            fixture.shape.draw(body, fixture)
    world.Step(TIMESTEP, 10, 10)
    pygame.display.flip()
    clock.tick(TARGET_FPS)