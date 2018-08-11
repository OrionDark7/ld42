import pygame, random #Python Modules
import objects, particles #Game Modules

print "(c) Copyright Orion Williams 2018 under the MIT Open-Source License"

def createTrash(amount):
    map = pygame.sprite.Group()
    for i in range(amount):
        map.add(objects.trash([random.randint(20, 780), random.randint(20, 580)]))
    return map

def createStars(amount):
    map = pygame.sprite.Group()
    for i in range(amount):
        map.add(particles.stars([random.randint(20, 780), random.randint(20, 580)]))
    return map

pygame.font.init()
pygame.joystick.init()
window = pygame.display.set_mode([800, 600])
window.fill([0, 0, 0])
running = True
controls = False
spaceship = objects.ship([400, 300])
pygame.key.set_repeat(1)
trash = createTrash(27)
stars = createStars(100)
font = pygame.font.Font(None, 24)
try:
    joystick = pygame.joystick.Joystick(0)
except:
    print "error"

joystick.init()
name = joystick.get_name()
print "Joystick Detected: {}".format(name)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if not controls:
                if event.key == pygame.K_UP:
                    spaceship.update("move", {"dir":"up"}, window)
                elif event.key == pygame.K_DOWN:
                    spaceship.update("move", {"dir": "down"}, window)
                elif event.key == pygame.K_LEFT:
                    spaceship.update("move", {"dir":"left"}, window)
                elif event.key == pygame.K_RIGHT:
                    spaceship.update("move", {"dir":"right"}, window)
            if event.key == pygame.K_a:
                controls = not controls
    if not event.type == pygame.KEYDOWN:
        spaceship.update("move", {"dir": "none"}, window)
    if controls:
        if joystick.get_axis(0) > 0.8:
            spaceship.update("move", {"dir": "right"}, window)
        elif joystick.get_axis(0) < -0.8:
            spaceship.update("move", {"dir": "left"}, window)
        if joystick.get_axis(1) > 0.8:
            spaceship.update("move", {"dir": "down"}, window)
        elif joystick.get_axis(1) < -0.8:
            spaceship.update("move", {"dir": "up"}, window)
        if joystick.get_axis(2) > 0.8:
            spaceship.update("move", {"dir": "right"}, window)
        elif joystick.get_axis(2) < -0.8:
            spaceship.update("move", {"dir": "left"}, window)
        if joystick.get_axis(3) > 0.8:
            spaceship.update("move", {"dir": "down"}, window)
        elif joystick.get_axis(3) < -0.8:
            spaceship.update("move", {"dir": "up"}, window)
    window.fill([0, 0, 0])
    stars.update(spaceship)
    stars.draw(window)
    trash.update(spaceship, trash)
    window.blit(spaceship.image, [spaceship.rect.left, spaceship.rect.top - 10])
    trash.draw(window)
    text = font.render("speed - x: " + str(spaceship.xvelocity) + " y: " + str(spaceship.yvelocity), 1, [255, 255, 255])
    window.blit(text, [10, 580])
    pygame.display.flip()
pygame.quit()