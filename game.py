import pygame, random, math #Python Modules
import objects, particles #Game Modules

print "(c) Copyright Orion Williams 2018 under the MIT Open-Source License"

def createTrash(amount):
    map = pygame.sprite.Group()
    for i in range(amount):
        pos = [random.randint(-29, 49)*40, random.randint(-21, 38)*40]
        map.add(objects.trash(pos))
    return map

def dumpTrash(amount):
    map = pygame.sprite.Group()
    dir = random.choice([-1, 1])
    for i in range(amount):
        if dir == -1:
            pos = [random.randint(2, 7)*40, (i + 6) * 40]
        elif dir == 1:
            pos = [random.randint(13, 18) * 40, (i + 6) * 40]
        map.add(objects.trash(pos))
    return map

def createStars(amount):
    map = pygame.sprite.Group()
    for i in range(amount):
        map.add(particles.stars([random.randint(20, 780), random.randint(20, 580)]))
    return map

def createPlanets(amount):
    map = pygame.sprite.Group()
    for i in range(amount):
        map.add(objects.planet(list([random.randint(-20 , 20)*60, random.randint(-15, 15)*60])))
    return map

def createBots(amount):
    map = pygame.sprite.Group()
    for i in range(amount):
        map.add(objects.bot(list([random.randint(-40, 40)*30, random.randint(-30, 30)*30])))
    return map

def checkAimer():
    global aimer
    if aimer[1] > 600:
        aimer[1] = 600
    elif aimer[1] < 0:
        aimer[1] = 0
    if aimer[0] > 800:
        aimer[0] = 800
    if aimer[0] < 0:
        aimer[0] = 0
    return aimer

class playArea(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.surface.Surface([3200, 2400])
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = -1200, -900
    def check(self, spaceship):
        self.rect.centerx -= spaceship.xvelocity*2
        self.rect.centery -= spaceship.yvelocity*2
        if not self.rect.colliderect(spaceship.rect):
            if spaceship.rect.centerx > self.rect.right:
                spaceship.xvelocity = -100
            elif spaceship.rect.centerx < self.rect.left:
                spaceship.xvelocity = 100
            if spaceship.rect.centery > self.rect.bottom:
                spaceship.yvelocity = -75
            elif spaceship.rect.centery < self.rect.top:
                spaceship.yvelocity = 75

class crosshairs(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image1 = pygame.transform.scale2x(pygame.image.load("./images/crosshair.png"))
        self.image2 = pygame.transform.scale2x(pygame.image.load("./images/crosshair-target.png"))
        self.image = self.image1
        self.rect = self.image.get_rect()
    def display(self):
        global window, aimer, bots, trash
        self.rect.centerx, self.rect.centery = aimer
        if pygame.sprite.spritecollide(self, trash, False):
            self.image = self.image2
        elif pygame.sprite.spritecollide(self, bots, False):
            self.image = self.image2
        else:
            self.image = self.image1
        window.blit(self.image, [self.rect.left, self.rect.top])

class button(pygame.sprite.Sprite):
    def __init__(self, text, pos, color, hcolor):
        pygame.sprite.Sprite.__init__(self)
        self.text = text
        self.font = pygame.font.Font("nulshock.bold.ttf", 18)
        self.image = self.font.render(str(self.text), 1, list(color))
        self.himage = self.font.render(str(self.text), 1, list(hcolor))
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = list(pos)
        self.midpoint = self.rect.width/2
        self.rectangle = pygame.surface.Surface([self.rect.width, 2])
        self.rectangle.fill(list(hcolor))
        self.clicked = False
    def display(self, window, mouse):
        if self.rect.collidepoint(list(mouse)):
            window.blit(self.himage, [self.rect.left, self.rect.top])
            window.blit(self.rectangle, [self.rect.left, self.rect.bottom-2])
        else:
            window.blit(self.image, [self.rect.left, self.rect.top])
    def check(self, mouse):
        if self.rect.collidepoint(list(mouse)):
            self.clicked = True
        else:
            self.clicked = False
        return self.clicked

def displaybar(percent, pos):
    global window
    for i in range(int(percent)):
        surf = pygame.surface.Surface([2, 10])
        surf.fill([255 - (i * 2.55), i * 2.55, 0])
        window.blit(surf, [pos[0] + (i * 2), pos[1]])
    pygame.display.flip()

def createCourse(level):
    orientation = random.choice(["h", "v"])
    if orientation == "h":
        course = objects.course("h", [-2400 - spaceship.scrollx, random.randint(-900+((level * 50) + 50), 900-((level * 50) + 50)) - spaceship.scrolly], (level * 50) + 50)
    elif orientation == "v":
        course = objects.course("v", [random.randint(-1200+((level * 50) + 50), 1200-((level * 50) + 50)) - spaceship.scrollx, -1800 - spaceship.scrolly], (level * 50) + 50)
    return course

pygame.font.init()
pygame.joystick.init()
window = pygame.display.set_mode([800, 600])
window.fill([0, 0, 0])
pygame.display.set_caption("O2 Space Salvage")
pygame.time.set_timer(pygame.USEREVENT + 1, 1000) #1 Second Timer
pygame.time.set_timer(pygame.USEREVENT + 2, 1000 / 5) #5 Bullet Shots per Second
running = True
controls = False
sense = 1
music = True
sounds = True
aimer = [0, 0]
screen = "menu"
level = 1
hit = False
prev = "menu"
time = 0
page = 1
msg = None
times = [120, 105, 90, 75, 60, 45, 30]
area = playArea()
crosshair = crosshairs() #I feel smart.
start = button("start game", [20, 250], [225, 225, 225], [255, 255, 255])
resume = button("resume game", [20, 250], [225, 225, 225], [255, 255, 255])
settings = button("game settings", [20, 280], [225, 225, 225], [255, 255, 255])
how = button("how to play", [20, 310], [225, 225, 225], [255, 255, 255])
quit = button("quit game", [20, 340], [225, 225, 225], [255, 255, 255])
back = button("back", [10, 10], [225, 225, 225], [255, 255, 255])
control = button("toggle", [20, 50], [255, 255, 255], [0, 225, 225])
sensitivity = button("toggle", [20, 80], [255, 255, 255], [0, 225, 225])
music_ = button("toggle", [20, 110], [255, 255, 255], [0, 255, 255])
sfx = button("toggle", [20, 140], [255, 255, 255], [0, 255, 255])
restart = button("restart", [350, 370], [225, 225, 225], [255, 255, 255])
next = button("next", [360, 570], [225, 225, 225], [255, 255, 255])
#pygame.mixer.music.load("./loops/salvage.mp3")
logo = pygame.image.load("./images/logo.png")
logo = pygame.transform.scale2x(logo)
logo = pygame.transform.scale2x(logo)
spaceship = objects.ship([400, 300])
pygame.key.set_repeat(10)
course = createCourse(level)
trash = createTrash(250)
stars = createStars(100)
planets = createPlanets(20)
bots = createBots(25)
bullets = pygame.sprite.Group()
clock = pygame.time.Clock()
font = pygame.font.Font("nulshock.bold.ttf", 18)
fontbig = pygame.font.Font("nulshock.bold.ttf", 36)
controller = True
mouse = []
try:
    joystick = pygame.joystick.Joystick(0)
except:
    controller = False

if controller:
    joystick.init()
    jname = joystick.get_name()

text = font.render("a ludum dare 42 entry", 1, [255, 255, 255])
window.blit(text, [260, 282])
pygame.display.flip()
pygame.time.delay(2000)
for i in stars:
    window.blit(i.image, [i.rect.left, i.rect.top])
    pygame.display.flip()

#IN WINDOWS
#music = pygame.mixer.Sound("./loops/menu.mp3")
#music.play(100)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if screen == "game":
                if event.key == pygame.K_ESCAPE:
                    screen = "pause"
                if not controls:
                    keys = pygame.key.get_pressed()
                    if keys[pygame.K_UP]:
                        spaceship.update("move", {"dir":"up"}, window)

                    elif keys[pygame.K_DOWN]:
                        spaceship.update("move", {"dir": "down"}, window)

                    elif keys[pygame.K_LEFT]:
                        spaceship.update("move", {"dir":"left"}, window)

                    elif keys[pygame.K_RIGHT]:
                        spaceship.update("move", {"dir":"right"}, window)

                    if keys[pygame.K_w]:
                        spaceship.update("move", {"dir":"up"}, window)

                    elif keys[pygame.K_s]:
                        spaceship.update("move", {"dir": "down"}, window)

                    elif keys[pygame.K_a]:
                        spaceship.update("move", {"dir":"left"}, window)

                    elif keys[pygame.K_d]:
                        spaceship.update("move", {"dir":"right"}, window)

                    if keys[pygame.K_e] and spaceship.type == "gun":
                        msg = "reloading..."
                        pygame.time.set_timer(pygame.USEREVENT+3, 1500)
                    elif keys[pygame.K_e] and spaceship.type == "vacuum" and spaceship.storage > 0:
                        msg = "dumping trash..."
                        pygame.time.set_timer(pygame.USEREVENT+3, 1500)
                    elif keys[pygame.K_e] and spaceship.type == "vacuum" and spaceship.storage <= 0:
                        msg = "no trash to dump!"
                        pygame.time.set_timer(pygame.USEREVENT+3, 1500)

                    if keys[pygame.K_SPACE]:
                        msg = "switching ships..."
                        pygame.time.set_timer(pygame.USEREVENT+3, 3000)
        if event.type == pygame.MOUSEMOTION:
            mouse = [event.pos[0], event.pos[1]]
            aimer = mouse
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:
                if screen == "game" and spaceship.loaded > 0 and spaceship.type == "gun":
                    aimer = [event.pos[0], event.pos[1]]
                    mouse = aimer
                    aimer = checkAimer()
                    spaceship.loaded -= 1
                    bullets.add(objects.bullet([400, 300], aimer))
                elif screen == "game" and spaceship.loaded <= 0 and spaceship.type == "gun":
                    msg = "out of ammo!"
                    pygame.time.set_timer(pygame.USEREVENT+3, 2000)
                if screen == "menu":
                    if start.check(mouse):
                        screen = "game"
                        spaceship.xvelocity = 0
                    if settings.check(mouse):
                        screen = "settings"
                        prev = "menu"
                    if how.check(mouse):
                        screen = "how"
                        prev = "menu"
                        page = 0
                    if quit.check(mouse):
                        running = False
                if screen == "pause":
                    if start.check(mouse):
                        screen = "game"
                        spaceship.xvelocity = 0
                    if settings.check(mouse):
                        screen = "settings"
                        prev = "pause"
                    if how.check(mouse):
                        screen = "how"
                        prev = "pause"
                        page = 0
                    if quit.check(mouse):
                        running = False
                if screen == "settings":
                    if back.check(mouse):
                        screen = prev
                    if control.check(mouse):
                        controls = not controls
                    if sensitivity.check(mouse) and not controls:
                        if sense == 1:
                            sense = 2
                            pygame.key.set_repeat(10)
                        elif sense == 2:
                            sense = 3
                            pygame.key.set_repeat(30)
                        elif sense == 3:
                            sense = 1
                            pygame.key.set_repeat(50)
                    if music_.check(mouse):
                        music = not music
                    if sfx.check(mouse):
                        sounds = not sounds
                if screen == "game over":
                    if restart.check(mouse):
                        level = 1
                        screen = "game"
                        trash = createTrash(250)
                        stars = createStars(100)
                        planets = createPlanets(20)
                        bots = createBots(25)
                        crosshair = crosshairs()
                        spaceship = objects.ship([400, 300])
                        area = playArea()
                        createCourse(level)
                        time = 0
                if screen == "how":
                    if back.check(mouse):
                        screen = prev
                    if next.check(mouse) and not page == 4:
                        page += 1
        if event.type == pygame.JOYAXISMOTION:
            if controls and controller:
                if joystick.get_axis(0) > 0.8:
                    spaceship.update("move", {"dir": "right"}, window)
                    hit = True
                elif joystick.get_axis(0) < -0.8:
                    spaceship.update("move", {"dir": "left"}, window)
                    hit = True
                if joystick.get_axis(1) > 0.8:
                    spaceship.update("move", {"dir": "down"}, window)
                    hit = True
                elif joystick.get_axis(1) < -0.8:
                    spaceship.update("move", {"dir": "up"}, window)
                    hit = True
                if joystick.get_axis(2) > 0.8:
                    aimer[0] += 10
                elif joystick.get_axis(2) < -0.8:
                    aimer[0] -= 10
                if joystick.get_axis(3) > 0.8:
                    aimer[1] += 10
                elif joystick.get_axis(3) < -0.8:
                    aimer[1] -= 10
        if event.type == pygame.JOYBUTTONDOWN:
                if joystick.get_button(13) == 1 and spaceship.type == "gun":
                    msg = "reloading..."
                    pygame.time.set_timer(pygame.USEREVENT+3, 1500)
                elif joystick.get_button(13) == 1 and spaceship.type == "vacuum" and spaceship.storage > 0:
                    msg = "dumping trash..."
                    pygame.time.set_timer(pygame.USEREVENT+3, 1500)
                elif joystick.get_button(13) == 1 and spaceship.type == "vacuum" and spaceship.storage <= 0:
                    msg = "no trash to dump!"
                    pygame.time.set_timer(pygame.USEREVENT+3, 1500)

        if event.type == pygame.USEREVENT+2:
            if controls and controller:
                if joystick.get_axis(5) > 0.8 and spaceship.loaded > 0 and spaceship.type == "gun":
                    spaceship.loaded -= 1
                    aimer = checkAimer()
                    bullets.add(objects.bullet([400, 300], aimer))
                elif joystick.get_axis(5) > 0.8 and spaceship.loaded <= 0 and spaceship.type == "gun":
                    msg = "out of ammo!"
                    pygame.time.set_timer(pygame.USEREVENT+3, 2000)
                if joystick.get_button(10) == 1 and screen == "game":
                    screen = "pause"
                elif joystick.get_button(10) == 1 and screen == "pause":
                    screen = "game"
                if joystick.get_button(14) == 1 and screen == "game":
                    msg = "switching ships..."
                    pygame.time.set_timer(pygame.USEREVENT+3, 3000)
        if event.type == pygame.USEREVENT+1 and screen == "game":
            time += 1
        if event.type == pygame.USEREVENT+3 and not msg == None:
            oldmsg = msg
            msg = None
            if oldmsg == "reloading...":
                spaceship.update("reload", {}, window)
            if oldmsg == "dumping trash...":
                newTrash = dumpTrash(spaceship.storage)
                trash.add(newTrash)
                spaceship.storage = 0
            if oldmsg == "switching ships...":
                if spaceship.type == "gun":
                    spaceship.type = "vacuum"
                elif spaceship.type == "vacuum":
                    spaceship.type = "plow"
                elif spaceship.type == "plow":
                    spaceship.type = "gun"
                msg = "ship type - " + spaceship.type
                pygame.time.set_timer(pygame.USEREVENT + 3, 1000)
                spaceship.update("change", {}, window)
            if oldmsg == "level cleared!":
                level += 1
                time = 0
                trash = createTrash(250)
                stars = createStars(100)
                planets = createPlanets(20)
                bots = createBots(25)
                crosshair = crosshairs()
                spaceship.xvelocity = 0
                spaceship.yvelocity = 0
                spaceship.scrollx = 0
                spaceship.scrolly = 0
                spaceship.storage = 0
                area = playArea()
                pygame.time.set_timer(pygame.USEREVENT + 1, 1000)
                course = createCourse(level)
                msg = "level " + str(level)
                pygame.time.set_timer(pygame.USEREVENT + 3, 3000)
                if spaceship.type == "plow":
                    spaceship.shield = 100
                if len(bots) <= 5:
                    newBots = createBots(20)
                    bots.add(newBots)
                if len(trash) <= 50:
                    newTrash = createTrash(200)
                    trash.add(newTrash)
    if screen == "game":
        if spaceship.shield <= 0:
            screen = "game over"
        if not event.type == pygame.KEYDOWN and not hit:
            spaceship.update("move", {"dir": "none"}, window)
            # if spaceship.facing == "left":
            #     spaceship.aiming = [-1, 0]
            # elif spaceship.facing == "right":
            #     spaceship.aiming = [1, 0]
            # elif spaceship.facing == "up":
            #     spaceship.aiming = [0, -1]
            # elif spaceship.facing == "down":
            #     spaceship.aiming = [0, 1]

        if len(bullets) > 0:
            bullets.update(spaceship)

        if course.clear and not msg == "level cleared!":
            pygame.time.set_timer(pygame.USEREVENT + 3, 3000)
            msg = "level cleared!"
        if not course.clear:
            course.update(trash, bots, spaceship)

        if time > times[level - 1] and level < 8:
            screen = "game over"
        elif time > times[6] and level >= 8:
            screen = "game over"

        window.fill([0, 0, 0])
        stars.update(spaceship)
        stars.draw(window)
        planets.update(spaceship)
        planets.draw(window)
        course.display(window)
        trash.update(spaceship, trash, bullets, bots, True)
        trash.update(spaceship, trash, bullets, bots, False)
        trash.draw(window)
        bullets.draw(window)
        bots.update(spaceship, bullets)
        bots.draw(window)
        window.blit(spaceship.image, [spaceship.rect.left, spaceship.rect.top - 10])
        area.check(spaceship)
        if not msg == None:
            text = font.render(msg, 1,
                               [255, 255, 255])
            rect = 400 - (text.get_rect().width/2)
            window.blit(text, [rect, 330])
        if len(str((times[level-1] - time) % 60)) == 1:
            text = font.render("time left: " + str(int(math.floor((times[level-1] - time) / 60)))+":0"+str((times[level-1] - time) % 60), 1,
                               [255, 255, 255])
        if len(str((times[level-1] - time) % 60)) == 2:
            text = font.render("time left: " + str(int(math.floor((times[level-1] - time) / 60)))+":"+str((times[level-1] - time) % 60), 1,
                               [255, 255, 255])
        if len(str((times[level-1] - time) % 60)) == 0:
            text = font.render("time left: " + str(int(math.floor((times[level-1] - time) / 60)))+":00", 1,
                               [255, 255, 255])
        window.blit(text, [620, 580])

        if spaceship.type == "gun":
            if spaceship.loaded > 0:
                color = [255, 255, 255]
            else:
                color = [255, 0, 0]
            text = font.render("ammo " + str(spaceship.loaded) + "/" + str(spaceship.ammo), 1, color)
            aimer = checkAimer()
            crosshair.display()
            window.blit(text, [10, 560])
        if spaceship.type == "vacuum":
            if spaceship.storage < 25:
                color = [255, 255, 255]
            else:
                color = [255, 0, 0]
            text = font.render("storage " + str(spaceship.storage) + "/25", 1, color)
            window.blit(text, [10, 560])
        text = font.render("shields:", 1,
                           [255, 255, 255])
        window.blit(text, [10, 580])
        displaybar(spaceship.shield, [120, 588])
        hit = False

    elif screen == "menu":
        window.fill([0, 0, 0])
        spaceship.xvelocity = 1
        stars.update(spaceship)
        stars.draw(window)
        start.display(window, mouse)
        settings.display(window, mouse)
        how.display(window, mouse)
        quit.display(window, mouse)
        window.blit(logo, [20, 20])

    elif screen == "game over":
        window.fill([0, 0, 0])
        spaceship.xvelocity = 0
        spaceship.yvelocity = 0
        stars.update(spaceship)
        stars.draw(window)
        planets.update(spaceship)
        planets.draw(window)
        trash.update(spaceship, trash, bullets, bots, False)
        trash.draw(window)
        bullets.draw(window)
        bots.update(spaceship, bullets)
        bots.draw(window)
        window.blit(spaceship.image, [spaceship.rect.left, spaceship.rect.top - 10])
        text = fontbig.render("game over", 1, [255, 255, 255])
        window.blit(text, [260, 318])
        restart.display(window, mouse)

    elif screen == "pause":
        window.fill([0, 0, 0])
        spaceship.xvelocity = 0
        spaceship.yvelocity = 0
        stars.update(spaceship)
        stars.draw(window)
        planets.draw(window)
        trash.draw(window)
        bullets.draw(window)
        bots.draw(window)
        window.blit(spaceship.image, [spaceship.rect.left, spaceship.rect.top - 10])
        window.blit(pygame.surface.Surface([200, 180]), [0, 200])
        resume.display(window, mouse)
        settings.display(window, mouse)
        how.display(window, mouse)
        quit.display(window, mouse)
        window.blit(logo, [20, 20])

    elif screen == "settings":
        window.fill([0, 0, 0])
        spaceship.xvelocity = 1
        stars.update(spaceship)
        stars.draw(window)
        back.display(window, mouse)
        control.display(window, mouse)
        if controls:
            text = font.render("controls: xbox controller", 1, [255, 255, 255])
        elif not controls:
            text = font.render("controls: keyboard", 1, [255, 255, 255])
        window.blit(text, [120, 50])
        if not controls:
            sensitivity.display(window, mouse)
            if sense == 1:
                text = font.render("sensitivity: high", 1, [255, 255, 255])
            elif sense == 2:
                text = font.render("sensitivity: medium", 1, [255, 255, 255])
            elif sense == 3:
                text = font.render("sensitivity: low", 1, [255, 255, 255])
            window.blit(text, [120, 80])
        music_.display(window, mouse)
        if music == True:
            text = font.render("music: on", 1, [255, 255, 255])
        elif music == False:
            text = font.render("music: off", 1, [255, 255, 255])
        window.blit(text, [120, 110])
        sfx.display(window, mouse)
        if sounds == True:
            text = font.render("sound effects: on", 1, [255, 255, 255])
        elif sounds == False:
            text = font.render("sound effects: off", 1, [255, 255, 255])
        window.blit(text, [120, 140])

    elif screen == "how":
        window.fill([0, 0, 0])
        spaceship.xvelocity = 1
        if page == 0:
            stars.update(spaceship)
            stars.draw(window)
            text = font.render("space. we always took it for granted. it's supposed", 1, [255, 255, 255])
            window.blit(text, [20, 50])
            text = font.render("be infinite... right? ironically with all the space debris, we", 1, [255, 255, 255])
            window.blit(text, [20, 70])
            text = font.render("are running out of space! space freighters that deliver", 1, [255, 255, 255])
            window.blit(text, [20, 90])
            text = font.render("supplies all over the galaxy can't get around anymore.", 1, [255, 255, 255])
            window.blit(text, [20, 110])
            text = font.render("as a solution to this, you and your younger", 1, [255, 255, 255])
            window.blit(text, [20, 130])
            text = font.render("brother started an initative designed to solve", 1, [255, 255, 255])
            window.blit(text, [20, 150])
            text = font.render("this problem, which you two called...", 1, [255, 255, 255])
            window.blit(text, [20, 170])
            window.blit(logo, [130, 200])
            back.display(window, mouse)
            next.display(window, mouse)
        elif page == 1:
            stars.update(spaceship)
            stars.draw(window)
            back.display(window, mouse)
            next.display(window, mouse)
            text = fontbig.render("goal of the game", 1, [255, 255, 255])
            window.blit(text, [180, 20])
            window.blit(pygame.image.load("./images/goal.png"), [200, 150])
            text = font.render("the goal of the game is to clear a path for", 1, [255, 255, 255])
            rect = (text.get_rect().width/2)
            window.blit(text, [400 - rect, 470])
            text = font.render("the space freigheter before it comes through.", 1, [255, 255, 255])
            rect = (text.get_rect().width / 2)
            window.blit(text, [400 - rect, 490])
            text = font.render("the path is highlighted in blue in-game.", 1, [255, 255, 255])
            rect = (text.get_rect().width / 2)
            window.blit(text, [400 - rect, 510])
        elif page == 2:
            stars.update(spaceship)
            stars.draw(window)
            back.display(window, mouse)
            next.display(window, mouse)
            text = fontbig.render("controls", 1, [255, 255, 255])
            window.blit(text, [260, 20])
            text = fontbig.render("keyboard", 1, [255, 255, 255])
            window.blit(text, [30, 70])
            text = fontbig.render("controller", 1, [255, 255, 255])
            window.blit(text, [430, 70])
            text = font.render("arrow keys - move", 1, [255, 255, 255])
            window.blit(text, [30, 130])
            text = font.render("wasd keys - move", 1, [255, 255, 255])
            window.blit(text, [30, 160])
            text = font.render("mouse - aim guns", 1, [255, 255, 255])
            window.blit(text, [30, 190])
            text = font.render("left click - fire guns", 1, [255, 255, 255])
            window.blit(text, [30, 220])
            text = font.render("space - change ship mode", 1, [255, 255, 255])
            window.blit(text, [30, 250])
            text = font.render("e - special actions", 1, [255, 255, 255])
            window.blit(text, [30, 280])
            window.blit(pygame.image.load("./images/controls-keyboard.png"), [0, 300])

            text = font.render("left joystick - move", 1, [255, 255, 255])
            window.blit(text, [430, 130])
            text = font.render("right joystick - aim guns", 1, [255, 255, 255])
            window.blit(text, [430, 160])
            text = font.render("right trigger - fire guns", 1, [255, 255, 255])
            window.blit(text, [430, 190])
            text = font.render("y button - change ship mode", 1, [255, 255, 255])
            window.blit(text, [430, 220])
            text = font.render("x button - special actions", 1, [255, 255, 255])
            window.blit(text, [430, 250])
            window.blit(pygame.image.load("./images/controls-controller.png"), [400, 300])
        elif page == 3:
            stars.update(spaceship)
            stars.draw(window)
            back.display(window, mouse)
            next.display(window, mouse)
            text = fontbig.render("cleaning up", 1, [255, 255, 255])
            window.blit(text, [240, 20])
            pygame.draw.line(window, [255, 255, 255], [0, 150], [800, 150], 2)
            pygame.draw.line(window, [255, 255, 255], [0, 330], [800, 330], 2)
            pygame.draw.line(window, [255, 255, 255], [0, 510], [800, 510], 2)
            window.blit(pygame.transform.scale2x(pygame.image.load("./images/s1/ship-l.png")), [30, 60])
            window.blit(pygame.transform.scale2x(pygame.image.load("./images/s2/ship-l.png")), [30, 200])
            window.blit(pygame.transform.scale2x(pygame.image.load("./images/s3/ship-l.png")), [30, 380])
            text = font.render("to switch between modes, press space on your keyboard", 1, [255, 255, 255])
            window.blit(text, [20, 520])
            text = font.render("or press x on your controller.", 1,
                               [255, 255, 255])
            window.blit(text, [20, 540])
            text = font.render("this is the default gunship.", 1,
                               [255, 255, 255])

            window.blit(text, [120, 60])
            text = font.render("it can shoot bullets at obstacles and robots.", 1,
                               [255, 255, 255])
            window.blit(text, [120, 80])
            text = font.render("it can shoot 25 bullets before reloading", 1,
                               [255, 255, 255])
            window.blit(text, [120, 100])
            text = font.render("it is vunerable to robots and space junk.", 1,
                               [255, 255, 255])
            window.blit(text, [120, 120])

            text = font.render("this is the vacuum ship.", 1,
                               [255, 255, 255])
            window.blit(text, [120, 190])
            text = font.render("it can suck up and hold space junk.", 1,
                               [255, 255, 255])
            window.blit(text, [120, 210])
            text = font.render("it can hold up to 25 pieces of junk.", 1,
                               [255, 255, 255])
            window.blit(text, [120, 230])
            text = font.render("it is vunerable to robots and space junk if", 1,
                               [255, 255, 255])
            window.blit(text, [120, 250])
            text = font.render("storage is full. it cannot fire bullets.",
                               1,
                               [255, 255, 255])
            window.blit(text, [120, 270])

            text = font.render("this is the plow ship.", 1,
                               [255, 255, 255])
            window.blit(text, [120, 370])
            text = font.render("it can push space junk out of the way very easily.", 1,
                               [255, 255, 255])
            window.blit(text, [120, 390])
            text = font.render("it cannot be harmed by space junk when in contact.", 1,
                               [255, 255, 255])
            window.blit(text, [120, 410])
            text = font.render("it is vunerable to robots, though less vunerable",
                               1,
                               [255, 255, 255])
            window.blit(text, [120, 430])
            text = font.render(
                "than other ships. it cannot fire bullets.",
                1,
                [255, 255, 255])
            window.blit(text, [120, 450])
        elif page == 4:
            stars.update(spaceship)
            stars.draw(window)
            back.display(window, mouse)
            text = fontbig.render("obstacles", 1, [255, 255, 255])
            window.blit(text, [220, 20])
            window.blit(pygame.transform.scale2x(pygame.image.load("./images/satellite.png")), [40, 130])
            window.blit(pygame.transform.scale2x(pygame.image.load("./images/shuttle.png")), [70, 190])
            window.blit(pygame.transform.scale2x(pygame.image.load("./images/rockets.png")), [70, 250])
            window.blit(pygame.transform.scale2x(pygame.image.load("./images/asteroid.png")), [70, 310])
            text = fontbig.render("space junk", 1, [255, 255, 255])
            window.blit(text, [30, 80])
            text = font.render("space junk is an obstacle that takes up", 1,
                               [255, 255, 255])
            window.blit(text, [152, 120])
            text = font.render("a lot of the map.it is generally small, but", 1,
                               [255, 255, 255])
            window.blit(text, [152, 140])
            text = font.render("is tedious to remove.", 1,
                               [255, 255, 255])
            window.blit(text, [152, 160])
            text = font.render("it can be destroyed by bullets, sucked by", 1,
                               [255, 255, 255])
            window.blit(text, [152, 180])
            text = font.render("a vacuum, or pushed by a plow. it can",
                               1,
                               [255, 255, 255])
            window.blit(text, [152, 200])
            text = font.render("also move slowly on its own in some situations.",
                               1,
                               [255, 255, 255])
            window.blit(text, [152, 220])

            text = fontbig.render("sentry bots", 1, [255, 255, 255])
            window.blit(text, [30, 380])
            window.blit(pygame.transform.scale2x(pygame.image.load("./images/bot.png")), [40, 460])
            window.blit(pygame.transform.scale2x(pygame.image.load("./images/bot-angry.png")), [120, 460])
            text = font.render("sentry bots are robots that can detect", 1,
                               [255, 255, 255])
            window.blit(text, [200, 440])
            text = font.render("ships from different ranges and", 1,
                               [255, 255, 255])
            window.blit(text, [200, 460])
            text = font.render("charge towards them and do", 1,
                               [255, 255, 255])
            window.blit(text, [200, 480])
            text = font.render("significant damage.", 1,
                               [255, 255, 255])
            window.blit(text, [200, 500])
            text = font.render("they can be killed by bullets.", 1,
                               [255, 255, 255])
            window.blit(text, [200, 520])

    pygame.display.flip()
pygame.quit()