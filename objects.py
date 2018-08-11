import pygame, random, os

print os.getcwd()

class ship(pygame.sprite.Sprite):
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.images = [pygame.image.load("./images/ship-l.png"),
                       pygame.image.load("./images/ship-lo.png"),
                       pygame.image.load("./images/ship-r.png"),
                       pygame.image.load("./images/ship-ro.png"),
                       pygame.image.load("./images/ship-u.png"),
                       pygame.image.load("./images/ship-uo.png"),
                       pygame.image.load("./images/ship-d.png")]
        self.image = pygame.image.load("./images/ship-l.png")
        self.surface = pygame.surface.Surface([40, 20])
        self.rect = self.surface.get_rect()
        self.rect.centerx, self.rect.centery = list(pos)
        self.xvelocity, self.yvelocity = 0, 0
        self.time = 0
    def update(self, action, info, screen):
        if action == "move":
            self.time += 1
            if info["dir"] == "down" and self.yvelocity < 16:
                if self.yvelocity <= 0:
                    self.yvelocity = 1
                elif not self.yvelocity > 16:
                    self.yvelocity += self.yvelocity
                self.image = self.images[6]
            if info["dir"] == "up" and self.yvelocity > -16:
                if self.yvelocity >= 0:
                    self.yvelocity = -1
                elif not self.yvelocity < -16:
                    self.yvelocity += self.yvelocity
                self.image = self.images[5]
            if info["dir"] == "right" and self.xvelocity < 16:
                if self.xvelocity <= 0:
                    self.xvelocity = 1
                elif not self.xvelocity > 16:
                    self.xvelocity += self.xvelocity
                self.image = self.images[3]
            if info["dir"] == "left" and self.xvelocity > -16:
                if self.xvelocity >= 0:
                    self.xvelocity = -1
                elif not self.yvelocity < -16:
                    self.xvelocity += self.xvelocity
                self.image = self.images[1]
            if info["dir"] == "none" and self.time % 8 == 0:
                if not self.xvelocity == 0:
                    self.xvelocity -= self.xvelocity/4
                if not self.yvelocity == 0:
                    self.yvelocity -= self.yvelocity/4
                if self.xvelocity == 3 or self.yvelocity == 1:
                    self.xvelocity = 0
                elif self.yvelocity == 3 or self.yvelocity == 1:
                    self.yvelocity = 0
            if self.xvelocity > 16 and self.yvelocity > 16:
                self.xvelocity, self.yvelocity =  16, 16
            elif self.xvelocity < -16 and self.yvelocity < -16:
                self.xvelocity, self.yvelocity = -16, -16
            self.rect.centerx += self.xvelocity/4
            self.rect.centery += self.yvelocity/4

class trash(pygame.sprite.Sprite):
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        image = random.choice(["./images/rockets.png", "./images/shuttle.png", "./images/satellite.png"])
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
        self.rect.centerx, self.rect.centery = list(pos)
        self.xvelocity, self.yvelocity = 0, 0
        self.time = 0
    def update(self, ship, trash):
        self.remove(trash)
        self.time += 1
        if self.rect.colliderect(ship.rect):
            self.xvelocity = ship.xvelocity
            self.yvelocity = ship.yvelocity
        if self.time % 10 == 0 and not self.rect.colliderect(ship.rect) and not pygame.sprite.spritecollide(self, trash, False):
            if not self.xvelocity == 0:
                self.xvelocity -= self.xvelocity / 4
            if not self.yvelocity == 0:
                self.yvelocity -= self.yvelocity / 4
            if self.xvelocity == 3 or self.yvelocity == 1:
                self.xvelocity = 0
            elif self.yvelocity == 3 or self.yvelocity == 1:
                self.yvelocity = 0
        elif pygame.sprite.spritecollide(self, trash, False):
            for i in trash:
                if self.rect.colliderect(i.rect):
                    self.xvelocity = i.xvelocity
                    self.yvelocity = i.yvelocity
                    break
        self.rect.centerx += self.xvelocity / 4
        self.rect.centery += self.yvelocity / 4
        self.add(trash)