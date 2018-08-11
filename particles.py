import pygame, random

class stars(pygame.sprite.Sprite):
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        radius = random.randint(2, 3)
        self.image = pygame.surface.Surface([radius, radius])
        self.image.fill([255, 255, 255])
        self.rect = self.image.get_rect()
        self.rect.centerx, self.rect.centery = list(pos)
        self.time = 0
    def update(self, spaceship):
        if self.rect.centerx > 800:
            self.rect.centerx = 0
            self.rect.centery = random.randint(0, 600)
        if self.rect.centerx < 0:
            self.rect.centerx = 800
            self.rect.centery = random.randint(0, 600)
        if self.rect.centery > 600:
            self.rect.centery = 0
            self.rect.centerx = random.randint(0, 800)
        if self.rect.centery < 0:
            self.rect.centery = 600
            self.rect.centerx = random.randint(0, 800)
        self.rect.centerx -= spaceship.xvelocity
        self.rect.centery -= spaceship.yvelocity