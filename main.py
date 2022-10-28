import pygame
import sys

pygame.init()
backround = pygame.image.load("img/hintergrund.png")
screen = pygame.display.set_mode((1200, 595))
clock = pygame.time.Clock()
pygame.display.set_caption("Ultra Krasser Mutterficker 3000")

attackLeft = pygame.image.load("img/attackLeft.png")
attackRight = pygame.image.load("img/attackRight.png")
jumping = pygame.image.load("img/sprung.png")
jumpsound = pygame.mixer.Sound("sounds/jump.wav")
goRight = [pygame.image.load("img/rechts1.png"),pygame.image.load("img/rechts2.png"),pygame.image.load("img/rechts3.png"),pygame.image.load("img/rechts4.png"),pygame.image.load("img/rechts5.png"),pygame.image.load("img/rechts6.png"),pygame.image.load("img/rechts7.png"),pygame.image.load("img/rechts8.png")]
goLeft = [pygame.image.load("img/links1.png"),pygame.image.load("img/links2.png"),pygame.image.load("img/links3.png"),pygame.image.load("img/links4.png"),pygame.image.load("img/links5.png"),pygame.image.load("img/links6.png"),pygame.image.load("img/links7.png"),pygame.image.load("img/links8.png")]
winSound = pygame.mixer.Sound("sounds/robosieg.wav")
loseSound = pygame.mixer.Sound("sounds/robotod.wav")
winPic = pygame.image.load("img/sieg.png")
losePic = pygame.image.load("img/verloren.png")



class Player:
    def __init__(self, x, y, speed, width, height, jump, direction, stepsLeft, stepsRight):
        self.x = x
        self.y = y
        self.speed = speed
        self.width = width
        self.height = height
        self.jump = jump
        self.direction = direction
        self.stepsLeft = stepsLeft
        self.stepsRight = stepsRight
        self.jumping = False
        self.lastDirection = [1,0]
        self.ok = True
    
    def run(self, list):
        if list[0]:
            self.x -= self.speed
            self.direction = [1,0,0,0]
            self.stepsLeft += 1
        if list[1]:
            self.x += self.speed
            self.direction = [0,1,0,0]
            self.stepsRight += 1
    
    def resetSchritte(self):
        self.stepsLeft = 0
        self.stepsRight = 0

    def standing(self):
        self.direction = [0,0,1,0]
        self.resetSchritte()
    
    def jumpSet(self):
        if self.jump == -16:
            self.jumping = True
            self.jump = 15
            pygame.mixer.Sound.play(jumpsound)
    
    def jumper(self):
        if self.jumping:
            self.direction = [0,0,0,1]
            if self.jump >= -15:
                n = 1
                if self.jump < 0:
                    n = -1
                self.y -= (self.jump ** 2) * 0.17 * n
                self.jump -= 1
            else:
                self.jumping = False
    
    def drawPlayer(self):
        if self.stepsLeft == 63:
            self.stepsLeft = 0
        if self.stepsRight == 63:
            self.stepsRight = 0

        if self.direction[0]:
            screen.blit(goLeft[self.stepsLeft//8], (self.x, self.y))
            self.lastDirection = [1,0]
        
        if self.direction[1]:
            screen.blit(goRight[self.stepsRight//8], (self.x, self.y))
            self.lastDirection = [0,1]
        
        if self.direction[2]:
            if self.lastDirection[0]:
                screen.blit(attackLeft, (self.x, self.y))
            else:
                screen.blit(attackRight, (self.x, self.y))
        
        if self.direction[3]:
            screen.blit(jumping, (self.x, self.y))

class Zombie:
    def __init__(self, x, y, speed, width, height, direction, xMin, xMax):
        self.x = x
        self.y = y
        self.speed = speed
        self.width = width
        self.height = height
        self.direction = direction
        self.stepsLeft = 0
        self.stepsRight = 0
        self.xMin = xMin
        self.xMax = xMax
        self.lives = 6
        self.leftList = [pygame.image.load("img/l1.png"),pygame.image.load("img/l2.png"),pygame.image.load("img/l3.png"),pygame.image.load("img/l4.png"),pygame.image.load("img/l5.png"),pygame.image.load("img/l6.png"),pygame.image.load("img/l7.png"),pygame.image.load("img/l8.png")]
        self.rightList = [pygame.image.load("img/r1.png"),pygame.image.load("img/r2.png"),pygame.image.load("img/r3.png"),pygame.image.load("img/r4.png"),pygame.image.load("img/r5.png"),pygame.image.load("img/r6.png"),pygame.image.load("img/r7.png"),pygame.image.load("img/r8.png")]
        self.full = pygame.image.load("img/voll.png")
        self.half = pygame.image.load("img/halb.png")
        self.empty = pygame.image.load("img/leer.png")
    
    def hearts(self):
        if self.lives >= 2:
            screen.blit(self.full, (507, 15))
        if self.lives >= 4:
            screen.blit(self.full, (569, 15))
        if self.lives == 6:
            screen.blit(self.full, (631, 15))
        
        if self.lives == 1:
            screen.blit(self.half, (507, 15))
        if self.lives == 3:
            screen.blit(self.half, (569, 15))
        if self.lives == 5:
            screen.blit(self.half, (631, 15))
        
        if self.lives <= 0:
            screen.blit(self.empty, (507, 15))
        if self.lives <= 2:
            screen.blit(self.empty, (569, 15))
        if self.lives <= 4:
            screen.blit(self.empty, (631, 15))

    def zdraw(self):
        if self.stepsLeft == 63:
            self.stepsLeft = 0
        if self.stepsRight == 63:
            self.stepsRight = 0

        if self.direction[0]:
            screen.blit(self.leftList[self.stepsLeft//8], (self.x, self.y))
        if self.direction[1]:
            screen.blit(self.rightList[self.stepsRight//8], (self.x, self.y))

    def run(self):
        self.x += self.speed
        if self.speed > 0:
            self.direction = [0,1]
            self.stepsRight += 1
        if self.speed < 0:
            self.direction = [1,0]
            self.stepsLeft += 1
    
    def leftRight(self):
        if self.x > self.xMax:
            self.speed *= -1
        elif self.x < self.xMin:
            self.speed *= -1
        self.run()
        
    


class bullet:
    def __init__(self, px, py, direct, rad, colour, speed):
        self.x = px
        self.y = py
        if direct[0]:
            self.x += 5
            self.speed = -1 * speed
        elif direct[1]:
            self.x += 92
            self.speed = speed
        self.y += 84
        self.rad = rad
        self.colour = colour
    
    def move(self):
        self.x += self.speed
    
    def draw(self):
        pygame.draw.circle(screen, self.colour, (self.x, self.y), self.rad, 0)

def redrawGameWindow():
    screen.blit(backround, (0, 0))
    for b in bullets:
        b.draw()
    player.drawPlayer()
    zombie.zdraw()
    zombie.hearts()
    if lose:
        screen.blit(losePic, (0, 0))
    elif win:
        screen.blit(winPic, (0, 0))
    pygame.display.update()

def bulletHandler():
    global bullets
    for k in bullets:
        if k.x >= 0 and k.x <= 1200:
            k.move()
        else:
            bullets.remove(k)

def collision():
    global bullets, lose, win, go
    zombieRect = pygame.Rect(zombie.x+18, zombie.y+24, zombie.width-36, zombie.height-24)
    playerbox = pygame.Rect(player.x+18, player.y+36, player.width-36, player.height-36)

    for b in bullets:
        bulletRect = pygame.Rect(b.x-b.rad, b.y-b.rad, b.rad*2, b.rad*2)
        if zombieRect.colliderect(bulletRect):
            bullets.remove(b)
            zombie.lives -= 1
            if zombie.lives <= 0 and not lose:
                win = True
                pygame.mixer.Sound.play(winSound)
                go = False
    
    if zombieRect.colliderect(playerbox):
        lose = True
        win = False
        pygame.mixer.Sound.play(loseSound)
        go = False
            

leftWall = pygame.draw.rect(screen, (0, 0, 0), (-1, 0, 2, 600), 0)
rightWall = pygame.draw.rect(screen, (0, 0, 0), (1199, 0, 2, 600), 0)
topWall = pygame.draw.rect(screen, (0, 0, 0), (0, -1, 1200, 2), 0)
go = True
lose = False
win = False
bullets = []

player = Player(300, 393, 5, 96, 128, -16, [0,0,1,0], 0, 0)
zombie = Zombie(600, 393, 4, 96, 128, [0,0], 40, 1090)

while go:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    playerbox = pygame.Rect(player.x, player.y, 96, 128)
    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT] and not playerbox.colliderect(leftWall):
        player.run([1,0])
    elif keys[pygame.K_RIGHT] and not playerbox.colliderect(rightWall):
        player.run([0,1])
    else:
        player.standing()
    
    if keys[pygame.K_UP] and not playerbox.colliderect(topWall):
        player.jumpSet()
    player.jumper()

    if keys[pygame.K_SPACE]:
        if len(bullets) <= 1 and player.ok:
            bullets.append(bullet(round(player.x), round(player.y), player.lastDirection, 8, (0, 0, 0), 7))
        player.ok = False

    if not keys[pygame.K_SPACE]:
        player.ok = True

    bulletHandler()
    zombie.leftRight()
    collision()
    redrawGameWindow()
    clock.tick(60)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
    redrawGameWindow()