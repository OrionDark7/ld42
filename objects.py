import pygame, random, os

class ship(pygame.sprite.Sprite):
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.imageset1 = [pygame.image.load("./images/s1/ship-l.png"),
                       pygame.image.load("./images/s1/ship-lo.png"),
                       pygame.image.load("./images/s1/ship-r.png"),
                       pygame.image.load("./images/s1/ship-ro.png"),
                       pygame.image.load("./images/s1/ship-u.png"),
                       pygame.image.load("./images/s1/ship-uo.png"),
                       pygame.image.load("./images/s1/ship-d.png")]
        self.imageset2 = [pygame.image.load("./images/s2/ship-l.png"),
                       pygame.image.load("./images/s2/ship-lo.png"),
                       pygame.image.load("./images/s2/ship-r.png"),
                       pygame.image.load("./images/s2/ship-ro.png"),
                       pygame.image.load("./images/s2/ship-u.png"),
                       pygame.image.load("./images/s2/ship-uo.png"),
                       pygame.image.load("./images/s2/ship-d.png")]
        self.imageset3 = [pygame.image.load("./images/s3/ship-l.png"),
                       pygame.image.load("./images/s3/ship-lo.png"),
                       pygame.image.load("./images/s3/ship-r.png"),
                       pygame.image.load("./images/s3/ship-ro.png"),
                       pygame.image.load("./images/s3/ship-u.png"),
                       pygame.image.load("./images/s3/ship-uo.png"),
                       pygame.image.load("./images/s3/ship-d.png")]
        self.images = self.imageset1
        self.image = pygame.image.load("./images/s1/ship-l.png")
        self.surface = pygame.surface.Surface([40, 20])
        self.rect = self.surface.get_rect()
        self.rect.centerx, self.rect.centery = list(pos)
        self.xvelocity, self.yvelocity = 0, 0
        self.time = 0
        self.facing = "left"
        self.index = 0
        self.aiming = [-1, 0]
        self.type = "gun"
        self.shield = 100
        self.ammo = 100
        self.loaded = 25
        self.storage = 0
        self.scrollx, self.scrolly = 0, 0
    def update(self, action, info, screen):
        if action == "change":
            if self.type == "gun":
                self.images = self.imageset1
                self.image = self.images[self.index]
            elif self.type == "vacuum":
                self.images = self.imageset2
                self.image = self.images[self.index]
            elif self.type == "plow":
                self.images = self.imageset3
                self.image = self.images[self.index]
        if action == "move":
            self.time += 1
            if info["dir"] == "down" and self.yvelocity < 8:
                if self.yvelocity <= 0:
                    self.yvelocity = 1
                elif not self.yvelocity > 8:
                    self.yvelocity += self.yvelocity
                self.image = self.images[6]
                self.index = 6
                self.aiming[1] = 1
            if info["dir"] == "up" and self.yvelocity > -8:
                if self.yvelocity >= 0:
                    self.yvelocity = -1
                elif not self.yvelocity < -8:
                    self.yvelocity += self.yvelocity
                self.image = self.images[5]
                self.index = 5
                self.aiming[1] = 0
            if info["dir"] == "right" and self.xvelocity < 8:
                if self.xvelocity <= 0:
                    self.xvelocity = 1
                elif not self.xvelocity > 8:
                    self.xvelocity += self.xvelocity
                self.image = self.images[3]
                self.index = 3
                self.aiming[0] = 1
            if info["dir"] == "left" and self.xvelocity > -8:
                if self.xvelocity >= 0:
                    self.xvelocity = -1
                elif not self.yvelocity < -8:
                    self.xvelocity += self.xvelocity
                self.image = self.images[1]
                self.index = 1
                self.aiming[0] = -1
            if info["dir"] == "none" and self.time % 6 == 0:
                if not self.xvelocity == 0:
                    if self.xvelocity < 0:
                        self.xvelocity += 2
                    else:
                        self.xvelocity -= 2
                if not self.yvelocity == 0:
                    if self.yvelocity < 0:
                        self.yvelocity += 2
                    else:
                        self.yvelocity -= 2
                if self.xvelocity == 3 or self.yvelocity == 1:
                    self.xvelocity = 0
                elif self.yvelocity == 3 or self.yvelocity == 1:
                    self.yvelocity = 0
                elif self.yvelocity == 1 or self.yvelocity == -1:
                    self.yvelocity = 0
            if self.xvelocity > 8 or self.yvelocity > 8:
                if self.xvelocity > 8:
                    self.xvelocity = 8
                elif self.yvelocity > 8:
                    self.yvelocity = 8
            elif self.xvelocity < -8 or self.yvelocity < -8:
                if self.xvelocity < -8:
                    self.xvelocity = -8
                elif self.yvelocity < -8:
                    self.yvelocity = -8
            if self.xvelocity == 0 or self.yvelocity == 0:
                if self.yvelocity == 0:
                    if self.image == self.images[5]:
                        self.image = self.images[4]
                        self.index = 4
                if self.xvelocity == 0:
                    if self.image == self.images[3]:
                        self.image = self.images[2]
                        self.index = 2
                    elif self.image == self.images[1]:
                        self.image = self.images[0]
                        self.index = 0
            if self.aiming[0] > 1:
                self.aiming[0] = 1
            if self.aiming[0] < -1:
                self.aiming[0] = -1
            if self.aiming[1] > 1:
                self.aiming[1] = 1
            if self.aiming[1] < -1:
                self.aiming[1] = -1
            self.scrollx += self.xvelocity
            self.scrolly += self.yvelocity
        if action == "reload":
            if self.loaded < 25:
                toload = 25 - self.loaded
                if self.ammo >= toload:
                    self.ammo -= toload
                    self.loaded += toload
                elif self.ammo <= toload:
                    self.loaded += self.ammo
                    self.ammo -= self.ammo

class bullet(pygame.sprite.Sprite):
    def __init__(self, pos, dir):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.surface.Surface([4, 4])
        self.image.fill([255, 0, 0])
        self.rect = self.image.get_rect()
        self.rect.centerx, self.rect.centery = list(pos)
        self.times = 0
        self.xvelocity, self.yvelocity = 0, 0
        if dir[0] > 400:
            self.xvelocity = -(400 - dir[0]) / 10
        if dir[0] < 400:
            self.xvelocity = -(400 - dir[0]) / 10
        if dir[1] > 300:
            self.yvelocity = -(300 - dir[1]) / 10
        if dir[1] < 300:
            self.yvelocity = -(300 - dir[1]) / 10
        # if dir[0] > 420:
        #     self.xvelocity = 10
        # elif dir[0] < 380:
        #     self.xvelocity = -10
        # if dir[1] > 330:
        #     self.yvelocity = 10
        # elif dir[1] < 280:
        #     self.yvelocity = -10
    def update(self, ship):
        self.times += 1
        if self.times > 50:
            self.kill()
        self.rect.centerx += self.xvelocity/2 - ship.xvelocity
        self.rect.centery += self.yvelocity/2 - ship.yvelocity

class trash(pygame.sprite.Sprite):
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        image = random.choice(["./images/rockets.png", "./images/shuttle.png", "./images/satellite.png", "./images/asteroid.png"])
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
        self.rect.centerx, self.rect.centery = list(pos)
        self.xvelocity, self.yvelocity = random.choice([-0.5 - 0.5, 0, 0, 0, 0, 0.5]), random.choice([-0.5, 0, 0, 0, 0, 0.5, 0.5])
        self.ox, self.oy = self.xvelocity, self.yvelocity
        self.roaming = True
        self.time = 0
        self.hit = False
    def update(self, ship, trash, bullets, bots, action):
        if action == True:
            self.remove(trash)
            if pygame.sprite.spritecollide(self, trash, False):
                self.ox = -self.ox
                self.oy = -self.oy
            else:
                self.rect.centerx += self.ox
                self.rect.centery += self.oy
            self.add(trash)
        else:
            self.remove(trash)
            self.time += 1
            if pygame.sprite.spritecollide(self, bots, False):
                self.xvelocity = 0
                self.yvelocity = 0
                self.roaming = False
            if ship.type == "plow":
                if not self.rect.colliderect(ship.rect):
                    self.xvelocity = -ship.xvelocity
                    self.yvelocity = -ship.yvelocity
                    self.hit = False
                elif self.rect.colliderect(ship.rect):
                    self.xvelocity = ship.xvelocity * 2
                    self.yvelocity = ship.yvelocity * 2
                    self.hit = True
                    self.roaming = False
            elif ship.type == "gun":
                if not self.rect.colliderect(ship.rect):
                    self.xvelocity = -ship.xvelocity
                    self.yvelocity = -ship.yvelocity
                    if self.hit:
                        ship.shield -= 0.25
                    self.hit = False
                elif self.rect.colliderect(ship.rect):
                    self.hit = True
                    self.xvelocity = ship.xvelocity * 2
                    self.yvelocity = ship.yvelocity * 2
                    self.roaming = False
            elif ship.type == "vacuum":
                if not self.rect.colliderect(ship.rect):
                    self.xvelocity = -ship.xvelocity
                    self.yvelocity = -ship.yvelocity
                if self.rect.centerx > 300 and self.rect.centerx < 500 and  self.rect.centery > 200 and self.rect.centery < 400 and ship.storage < 25:
                    self.xvelocity = (400 - self.rect.centerx) / 10
                    self.yvelocity = (300 - self.rect.centery) / 10
                    self.roaming = False
            if self.time % 10 == 0 and not self.rect.colliderect(ship.rect) and not self.roaming:
                if self.roaming == False:
                    if self.xvelocity > 0:
                        self.xvelocity -= 1
                    elif self.xvelocity < 0:
                        self.xvelocity += 1
                    if self.yvelocity > 0:
                        self.yvelocity -= 1
                    elif self.yvelocity < 0:
                        self.yvelocity += 1
            self.rect.centerx += -ship.xvelocity + self.xvelocity
            self.rect.centery += -ship.yvelocity + self.yvelocity
            if not pygame.sprite.spritecollide(self, bullets, False) and ship.type == "gun":
                self.add(trash)
            elif pygame.sprite.spritecollide(self, bullets, False) and ship.type == "gun":
                if random.randint(1, 10) == 1 and not ship.shield >= 100:
                    ship.shield += 2
            if ship.type == "vacuum" and not self.rect.colliderect(ship.rect):
                self.add(trash)
            elif ship.type == "vacuum" and self.rect.colliderect(ship.rect) and ship.storage < 25:
                ship.storage += 1
            elif ship.type == "vacuum" and self.rect.colliderect(ship.rect) and ship.storage >= 25:
                ship.shield -= 0.25
                self.add(trash)
            elif ship.type == "plow":
                self.add(trash)

class planet(pygame.sprite.Sprite):
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        size = random.randint(30, 70)
        self.image = pygame.image.load("./images/planet" + str(random.randint(1, 4)) + ".png")
        self.image = pygame.transform.scale(self.image, [size, size])
        self.rect = self.image.get_rect()
        self.rect.centerx, self.rect.centery = list(pos)
        self.time = 0
    def update(self, spaceship):
        self.rect.centerx -= spaceship.xvelocity
        self.rect.centery -= spaceship.yvelocity

class bot(pygame.sprite.Sprite):
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image1 = pygame.image.load("./images/bot.png")
        self.image2 = pygame.image.load("./images/bot-angry.png")
        self.image = self.image1
        self.rect = self.image.get_rect()
        self.rect.centerx, self.rect.centery = list(pos)
        self.xvelocity, self.yvelocity = 0, 0
        self.range = random.randint(100, 200)
    def update(self, spaceship, bullets):
        self.rect.centerx += ((-spaceship.xvelocity + self.xvelocity)*2)
        self.rect.centery += ((-spaceship.yvelocity + self.yvelocity)*2)
        if bool(self.rect.centerx < 400+self.range and self.rect.centerx > 400-self.range and self.rect.centery > 300-self.range and self.rect.centery < 300+self.range):
            self.xvelocity = (400 - self.rect.centerx) / 20
            self.yvelocity = (300 - self.rect.centery) / 20
            self.image = self.image2
        if self.rect.centerx < 420 and self.rect.centerx > 380 and self.rect.centery < 320 and self.rect.centery > 280:
            self.xvelocity = 0
            self.yvelocity = 0
            self.image = self.image1
        elif self.rect.centerx > 400+self.range or self.rect.centerx < 400-self.range or self.rect.centery < 300-self.range or self.rect.centery > 300+self.range:
            self.xvelocity = 0
            self.yvelocity = 0
            self.image = self.image1
        if self.rect.colliderect(spaceship.rect):
            self.kill()
            if spaceship.type == "plow":
                spaceship.shield -= 5
            else:
                spaceship.shield -= 10
        if pygame.sprite.spritecollide(self, bullets, False):
            self.kill()
            if random.randint(1, 10) < 5:
                spaceship.ammo += 5

class course(pygame.sprite.Sprite):
    def __init__(self, orientation, pos, width):
        pygame.sprite.Sprite.__init__(self)
        if orientation == "h":
            self.image = pygame.surface.Surface([6400, width])
            self.image.fill([107, 190, 255])
        if orientation == "v":
            self.image = pygame.surface.Surface([width, 4800])
            self.image.fill([107, 190, 255])
        self.image.set_alpha(200)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = list(pos)
        self.clear = False
    def update(self, trash, bots, ship):
        self.rect.centerx += -ship.xvelocity * 2
        self.rect.centery += -ship.yvelocity * 2
        if pygame.sprite.spritecollide(self, trash, False) or pygame.sprite.spritecollide(self, bots, False):
            self.clear = False
        else:
            self.clear = True
    def display(self, window):
        window.blit(self.image, [self.rect.left, self.rect.top])