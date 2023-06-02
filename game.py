import pygame
import random
import threading
import time
#import all the images
w = 300
if True:
    blue_ghostA = pygame.image.load(r"images\blue_ghost.png")
    blue_ghost = pygame.transform.scale(blue_ghostA, (w, w))
    blue_ghost_B = pygame.image.load(r"images\blue_ghost_mirror.png")
    blue_ghost_mirror = pygame.transform.scale(blue_ghost_B, (w, w))
    blue_ghost_gunA = pygame.image.load(r"images\blue_ghost_gun.png")
    blue_ghost_gun = pygame.transform.scale(blue_ghost_gunA, (w, w))
    blue_ghost_gunM = pygame.image.load(r"images\blue_ghost_gun_mirror.png")
    blue_ghost_gun_mirror = pygame.transform.scale(blue_ghost_gunM, (w, w))
    blue_ghost_swordA = pygame.image.load(r"images\blue_ghost_sword.png")
    blue_ghost_sword = pygame.transform.scale(blue_ghost_swordA, (w, w))
    blue_ghost_swordM = pygame.image.load(r"images\blue_ghost_sword_mirror.png")
    blue_ghost_sword_mirror = pygame.transform.scale(blue_ghost_swordM, (w, w))
    blue_ghost_slashA = pygame.image.load(r"images\blue_ghost_slash.png")
    blue_ghost_slash = pygame.transform.scale(blue_ghost_slashA, (w, w))
    blue_ghost_slashM = pygame.image.load(r"images\blue_ghost_slash_mirror.png")
    blue_ghost_slash_mirror = pygame.transform.scale(blue_ghost_slashM, (w, w))

    red_ghostA = pygame.image.load(r"images\red_ghost.png")
    red_ghost = pygame.transform.scale(red_ghostA, (w, w))
    red_ghost_B = pygame.image.load(r"images\red_ghost_mirror.png")
    red_ghost_mirror = pygame.transform.scale(red_ghost_B, (w, w))
    red_ghost_gunA = pygame.image.load(r"images\red_ghost_gun.png")
    red_ghost_gun = pygame.transform.scale(red_ghost_gunA, (w, w))
    red_ghost_gunM = pygame.image.load(r"images\red_ghost_gun_mirror.png")
    red_ghost_gun_mirror = pygame.transform.scale(red_ghost_gunM, (w, w))
    red_ghost_swordA = pygame.image.load(r"images\red_ghost_sword.png")
    red_ghost_sword = pygame.transform.scale(red_ghost_swordA, (w, w))
    red_ghost_swordM = pygame.image.load(r"images\red_ghost_sword_mirror.png")
    red_ghost_sword_mirror = pygame.transform.scale(red_ghost_swordM, (w, w))
    red_ghost_slashA = pygame.image.load(r"images\red_ghost_slash.png")
    red_ghost_slash = pygame.transform.scale(red_ghost_slashA, (w, w))
    red_ghost_slashM = pygame.image.load(r"images\red_ghost_slash_mirror.png")
    red_ghost_slash_mirror = pygame.transform.scale(red_ghost_slashM, (w, w))

# Set up the display
pygame.init()
pygame.display.set_caption("Game")
screen = pygame.display.set_mode((840, 680))
clock = pygame.time.Clock()

# important values
gameWidth = screen.get_width()-20
gameHeight = screen.get_height()-65
gameX = 10
gameY = 45
groundY = gameY+gameHeight-60
speed = 1.3
offScreen = 125
blueHealthPos = screen.get_width()-310
swordDamage = 13
randomDiff = 6
gunDamage = 8
hb = 108
swordWidth = 36
swX = 43
cooldown = 0.44
floor = groundY-w
BLUE = (50, 50, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
gameover = False
stunTime = 0.4
# Update the screen
pygame.display.flip()




#player class
class Player:
    def __init__(self, color):
        self.color = color
        self.image = None
        self.x = None
        self.y = None
        self.dy = None
        self.dx = None
        self.ghost = None
        self.mirror = None
        self.gun = None
        self.gun_mirror = None
        self.sword = None
        self.sword_mirror = None
        self.slash = None
        self.slash_mirror = None
        self.left = None
        self.right = None
        self.equipSword = None
        self.attack = None
        self.equipGun = None
        self.jump = None
        if color == "blue":
            self.ghost = blue_ghost
            self.mirror = blue_ghost_mirror
            self.gun_mirror = blue_ghost_gun_mirror
            self.gun = blue_ghost_gun
            self.sword = blue_ghost_sword
            self.sword_mirror = blue_ghost_sword_mirror
            self.slash = blue_ghost_slash
            self.slash_mirror = blue_ghost_slash_mirror
            self.left = pygame.K_LEFT
            self.right = pygame.K_RIGHT
            self.equipSword = pygame.K_j
            self.attack = pygame.K_k
            self.equipGun = pygame.K_l
            self.jump = pygame.K_UP
            self.reset()

        elif color == "red":
            self.health = 300
            self.dy = 0
            self.dx = 0
            self.ghost = red_ghost
            self.mirror = red_ghost_mirror
            self.gun_mirror = red_ghost_gun_mirror
            self.gun = red_ghost_gun
            self.sword = red_ghost_sword
            self.sword_mirror = red_ghost_sword_mirror
            self.slash = red_ghost_slash
            self.slash_mirror = red_ghost_slash_mirror
            self.left = pygame.K_a
            self.right = pygame.K_d
            self.equipSword = pygame.K_x
            self.attack = pygame.K_c
            self.equipGun = pygame.K_v
            self.jump = pygame.K_w
            self.image = red_ghost
            self.x = gameX+40
            self.y = groundY-w
            self.is_attacking = False
            self.reset()
        else:
            raise Exception("cannot be neither blue nor red ghost")
    
    def stunHelper(self):
        time.sleep(stunTime)
    
    def stun(a):
        print("stunning")
        a.stunHelper()

    def reset(self):
        if self.color == ("blue"):
            self.health = 300
            self.dy = 0
            self.dx = 0
            self.image = blue_ghost_mirror
            self.x = gameX+gameWidth-40-w
            self.y = groundY-w
            self.is_attacking = False
        elif self.color == ("red"):
            self.health = 300
            self.dy = 0
            self.dx = 0
            self.image = red_ghost
            self.x = gameX+40
            self.y = groundY-w
            self.is_attacking = False
        else:
            raise Exception("cannot be niether blue nor red ghost")

    def attackMethod(self, enemy):
        global swordDamage, gunDamage, blueHealthPos
        if not self.is_attacking:
            #facing right
            self.is_attacking = True
            if self.image == self.sword:
                self.image = self.slash
                swordX = self.x+w-swX
                swordY = self.y+(w/2)
                if swordX>=enemy.x+hb and swordX-swordWidth<=enemy.x+w-hb and swordY>=enemy.y+70 and swordY<=enemy.y+w:
                    randomDamage = random.randint(0,randomDiff)
                    enemy.health = enemy.health-(swordDamage+randomDamage)
                    if enemy.color == "blue":
                        blueHealthPos = blueHealthPos +(swordDamage+randomDamage)
                time.sleep(cooldown/2+0.01)
                self.image = self.sword
                time.sleep(cooldown/2-0.06)

            #facing left
            if self.image == self.sword_mirror:
                self.image = self.slash_mirror
                swordX = self.x+swX
                swordY = self.y+(w/2)
                if swordX<= enemy.x+w-hb and swordX+swordWidth>=enemy.x+hb and swordY>=enemy.y+70 and swordY<=enemy.y+w:
                    randomDamage = random.randint(0,randomDiff)
                    enemy.health = enemy.health-(swordDamage+randomDamage)
                    if enemy.color == "blue":
                        blueHealthPos = blueHealthPos+(swordDamage+randomDamage)
                time.sleep(cooldown/2+0.01)
                self.image = self.sword_mirror
                time.sleep(cooldown/2-0.06)
            if self.image == self.gun:
                pass
            if self.image == self.gun_mirror:
                pass
            self.is_attacking = False
            
    def equip_sword(self):
        if self.image == self.ghost or self.image == self.slash or self.image == self.gun:
            self.image = self.sword
        elif self.image == self.mirror or self.image == self.gun_mirror or self.image == self.slash_mirror:
            self.image = self.sword_mirror
        elif self.image == self.sword:
            self.image = self.ghost
        elif self.image == self.sword_mirror:
            self.image = self.mirror
        else:
            raise Exception("Unrecognized image")
        time.sleep(0.1)
    def equip_gun(self):
        if self.image == self.ghost or self.image == self.slash or self.image == self.sword:
            self.image = self.gun
        elif self.image == self.mirror or self.image == self.sword_mirror or self.image == self.slash_mirror:
            self.image = self.gun_mirror
        elif self.image == self.gun:
            self.image = self.ghost
        elif self.image == self.gun_mirror:
            self.image = self.mirror
        else:
            raise Exception("Unrecognized image")
    def turn(self, direction):
        if direction=="left":
            if self.image == self.ghost:
                self.image = self.mirror
            elif self.image == self.gun:
                self.image = self.gun_mirror
            elif self.image == self.sword:
                self.image = self.sword_mirror
            elif self.image == self.slash:
                self.image = self.slash_mirror
        if direction=="right":
            if self.image == self.mirror:
                self.image = self.ghost
            elif self.image == self.gun_mirror:
                self.image = self.gun
            elif self.image == self.sword_mirror:
                self.image = self.sword
            elif self.image == self.slash_mirror:
                self.image = self.slash
    def renderGravity(self):
        global floor
        gravity = 0.0141
        if self.onFloor():
            self.y = floor
            self.dy = 0
        else:
            self.dy += gravity
    def onFloor(self):
        return self.y >= floor
    def jumpMethod(self):
        jumpPower = 2.3
        if not self.onFloor():
            return
        self.dy -= jumpPower

    def render(self, enemy):
        global speed, running, gameover
        while self.health>0 and running:
            time.sleep(0.001)
            keys = pygame.key.get_pressed()
            if keys[self.attack]:
                if not self.is_attacking:
                    self.attackMethod(enemy)
                else:
                    self.is_attacking = False
            if keys[self.equipSword]:
                self.equip_sword()
            if keys[self.left]:
                #move left
                self.dx = -speed
                self.turn("left")
                if self.x<=(-1*offScreen)-20:
                    self.x = screen.get_width()+offScreen
                pygame.draw.rect(screen, (50, 50, 255), (gameX-15, gameY, 15, gameHeight))

            elif keys[self.right]:
                self.dx = speed
                self.turn("right")
                if self.x >=offScreen+screen.get_width():
                    self.x = offScreen*-1
            else:
                self.dx = 0
            if keys[self.jump]:
                self.jumpMethod()
            pygame.draw.rect(screen, (50, 50, 255), (gameX-15, gameY, 15, gameHeight))
            self.x += self.dx
            self.y += self.dy
            self.renderGravity()
        gameover = True

    def display(self):
        screen.blit(self.image, (self.x, self.y))

def drawBG():
    pygame.draw.rect(screen, (50, 50, 255), (0,0,840,680))
    pygame.draw.rect(screen, (0, 0, 0), (gameX, gameY, gameWidth, gameHeight))
    pygame.draw.rect(screen, (50, 50, 50), (10, 10, 300, 25))
    pygame.draw.rect(screen, (255, 0, 0), (10, 10, red.health, 25)) #redHealth
    pygame.draw.rect(screen, (50, 50, 50), (screen.get_width()-310, 10, 300, 25))
    pygame.draw.rect(screen, (0, 230, 255), (blueHealthPos, 10, blue.health, 25)) #blueHealth
    pygame.draw.rect(screen, (0, 50, 0), (gameX, groundY, gameWidth, 60))

def gameOverScreen():
    time.sleep(1)
    global BLUE, RED, GREEN, blueHealthPos
    pygame.draw.rect(screen, (0, 0, 0), (gameX, gameY, gameWidth, gameHeight))
    font = pygame.font.Font(None, 72)
    winner_text_render = pygame.Surface((0,0))
    winner_text_rect = winner_text_render.get_rect(center=(gameX+(gameWidth/2), gameY+(gameHeight/2)-50))
    if blue.health<0 and red.health<0:
        pygame.draw.rect(screen, (50, 50, 50), (screen.get_width()-310, 10, 300, 25))
        pygame.draw.rect(screen, (50, 50, 50), (10, 10, 300, 25))
        pygame.display.flip()
        winner_text = "Everyone Lost"
        font_color = GREEN
        winner_text_render = font.render(winner_text, True, font_color)
        winner_text_rect = winner_text_render.get_rect(center=(gameX+(gameWidth/2), gameY+(gameHeight/2)-50))
    elif blue.health<0:
        winner_text = "Red Player Wins!"
        font_color = RED
        winner_text_render = font.render(winner_text, True, font_color)
        winner_text_rect = winner_text_render.get_rect(center=(gameX+(gameWidth/2), gameY+(gameHeight/2)-50))
        pygame.draw.rect(screen, (50, 50, 50), (screen.get_width()-310, 10, 300, 25))
        pygame.display.flip()
    elif red.health<0:
        winner_text = "Blue Player Wins!"
        font_color = BLUE
        winner_text_render = font.render(winner_text, True, font_color)
        winner_text_rect = winner_text_render.get_rect(center=(gameX+(gameWidth/2), gameY+(gameHeight/2)-50))
        pygame.draw.rect(screen, (50, 50, 50), (10, 10, 300, 25))
        pygame.display.flip()
    playAgainText = "Press space to play again"
    font = pygame.font.Font(None, 64)
    font_color = GREEN
    againTextRender = font.render(playAgainText, True, font_color)
    again_text_rect = againTextRender.get_rect(center=(gameX + gameWidth / 2, gameY + gameHeight / 2 + 100))
    screen.blit(againTextRender, again_text_rect.topleft)
    screen.blit(winner_text_render, winner_text_rect.topleft)
    pygame.display.flip()



running = True
def renderGame():
    global running
    running = True
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                running = False
                break
        blue.reset()
        red.reset()
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    running = False
                    break
            if not gameover:
                drawBG()
                blue.display()
                red.display()
                pygame.draw.rect(screen, (50, 50, 255), (gameX+gameWidth, gameY, 15, gameHeight))
                pygame.draw.rect(screen, (50, 50, 255), (gameX-15, gameY, 15, gameHeight))
            else:
                running = False
                break
            pygame.display.flip()
        gameOverScreen()
        flagVariable = True
        while flagVariable:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    flagVariable = False
                    running = False
                    break
                keys = pygame.key.get_pressed()
                if keys[pygame.K_SPACE]:
                    flagVariable = False
                    running = True
                    break


def gameLoop():
    global running
    running = True
    global gameover
    gameover = False


    redThread = threading.Thread(target=red.render, args=[blue])
    blueThread = threading.Thread(target=blue.render, args=[red])

    redThread.start()
    blueThread.start()
    while running:
        renderGame()
    redThread.join()
    blueThread.join()



# Run the game
blue = Player("blue")
red = Player("red")
while True:
    gameLoop()
    '''keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        pass
    else:
        time.sleep(0.1)'''