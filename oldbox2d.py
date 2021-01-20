import pygame
from Box2D.b2 import world, polygonShape, circleShape, staticBody, dynamicBody

TARGET_FPS = 60
PPM = 20
TIMESTEP = 1.0 / TARGET_FPS

SCREEN_WIDTH, SCREEN_HEIGHT = 640, 400

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
pygame.display.set_caption("aaaa")
clock = pygame.time.Clock()

world = world(gravity=(0, -10))

ground_body = world.CreateStaticBody(position=(0,0), shapes=polygonShape(box=(50, 1)))
for x in range(5, 30, 5):
    body = world.CreateDynamicBody(position=(x, 20))
    circle = body.CreateCircleFixture(radius=1, density=1, friction=0.3)
for x in range(5, 40, 4):
    body = world.CreateDynamicBody(position=(x, 30), angle=x)
    box = body.CreatePolygonFixture(box=(2, 1), density=1, friction=0.3)
colors = {
    staticBody: (255, 255, 255, 255),
    dynamicBody: (127, 127, 127, 255)
}


def my_draw_polygon(polygon, body, fixture):
    vertices = [(body.transform * v) * PPM for v in polygon.vertices]
    vertices = [(v[0], SCREEN_HEIGHT - v[1]) for v in vertices]
    pygame.draw.polygon(screen, colors[body.type], vertices)


polygonShape.draw = my_draw_polygon


def my_draw_circle(circle, body, fixture):
    position = body.transform * circle.pos * PPM
    position = (position[0], SCREEN_HEIGHT - position[1])
    pygame.draw.circle(screen, colors[body.type], [int(x) for x in position], int(circle.radius * PPM))


circleShape.draw = my_draw_circle

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