import pygame
from pygame import mixer
from pygame.locals import *
import random


pygame.mixer.pre_init(44100, -16, 2, 512)
mixer.init()
pygame.init()


# fps
clock = pygame.time.Clock()
fps = 60


screenWidth = 600
screenHeight = 800

screen = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption('Space Invaders')


# fonts
fontSmall = pygame.font.SysFont('Constantia', 30)
fontBig = pygame.font.SysFont('Constantia', 40)


# sounds
explosion1 = pygame.mixer.Sound("explosion.wav")
explosion1.set_volume(0.25)

explosion2 = pygame.mixer.Sound("explosion2.wav")
explosion2.set_volume(0.25)

laser = pygame.mixer.Sound("laser.wav")
laser.set_volume(0.25)


# game variables
rows = 5
columns = 5
alien_cooldown = 1000  # bullet cooldown in milliseconds
finalAlienShot = pygame.time.get_ticks()
countdown = 3
finalCount = pygame.time.get_ticks()
gameOver = 0  # 0 is no game over, 1 means player has won, -1 means player has lost

# color variables
red = (255, 0, 0)
green = (0, 255, 0)
white = (255, 255, 255)

# loading image
bg = pygame.image.load("bg.png")

def draw_bg():
    screen.blit(bg, (0, 0))

# text creation
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

# spaceship class
class Spaceship(pygame.sprite.Sprite):
    def __init__(self, x, y, health):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("spaceship.png")
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.startingHealth = health
        self.remainingHealth = health
        self.lastShot = pygame.time.get_ticks()


    def update(self):
        # set movement speed
        speed = 8
        # set a cooldown variable
        cooldown = 500  # milliseconds
        gameOver = 0


        # get keys pressed
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= speed
        if key[pygame.K_RIGHT] and self.rect.right < screenWidth:
            self.rect.x += speed

        # current time
        timeNow = pygame.time.get_ticks()
        # shooting bullet
        if key[pygame.K_SPACE] and timeNow - self.lastShot > cooldown:
            laser.play()
            bullet = Bullets(self.rect.centerx, self.rect.top)
            bulletGroup.add(bullet)
            self.lastShot = timeNow

        # mask
        self.mask = pygame.mask.from_surface(self.image)

        # health bar
        pygame.draw.rect(screen, red, (self.rect.x, (self.rect.bottom + 10), self.rect.width, 15))
        if self.remainingHealth > 0:
            pygame.draw.rect(screen, green, (self.rect.x, (self.rect.bottom + 10), int(self.rect.width * (self.remainingHealth / self.startingHealth)), 15))
        elif self.remainingHealth <= 0:
            explosion = Explosion(self.rect.centerx, self.rect.centery, 3)
            explosionGroup.add(explosion)
            self.kill()
            gameOver = -1
        return gameOver

    
    
# bullets
class Bullets(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("bullet.png")
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

    def update(self):
        self.rect.y -= 5
        if self.rect.bottom < 0:
            self.kill()
        if pygame.sprite.spritecollide(self, alienGroup, True):
            self.kill()
            explosion1.play()
            explosion = Explosion(self.rect.centerx, self.rect.centery, 2)
            explosionGroup.add(explosion)


# shield
class Shield(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((50, 50))
        pygame.draw.rect(self.image, (0, 255, 0), (0, 0, self.image.get_width(), self.image.get_height()))
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.health = 4

    def update(self):
        if pygame.sprite.spritecollide(self, alienBulletGroup, True):
            self.health -= 1
            explosion1.play()
            explosion = Explosion(self.rect.centerx, self.rect.centery, 2)
            explosionGroup.add(explosion)
            # change the shield color to signify that it has been hit
            pygame.draw.rect(self.image, (0, 0, 0), (0, 0, self.image.get_width(), self.image.get_height()))
            pygame.draw.rect(self.image, (0, 255, 60 * (4 - self.health)), (0, 0, self.image.get_width(), self.image.get_height()))

        if self.health <= 0:
            self.kill()

# alien
class Aliens(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("alien" + str(random.randint(1, 5)) + ".png")
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.move_counter = 0
        self.move_direction = 1

    def update(self):
        self.rect.x += self.move_direction
        self.move_counter += 1
        if abs(self.move_counter) > 75:
            self.move_direction *= -1
            self.move_counter *= self.move_direction

            

# alien's bullets
class Alien_Bullets(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("alien_bullet.png")
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

    def update(self):
        self.rect.y += 2
        if self.rect.top > screenHeight:
            self.kill()
        if pygame.sprite.spritecollide(self, spaceshipGroup, False, pygame.sprite.collide_mask):
            self.kill()
            explosion2.play()
            # reduce spaceship health
            spaceship.remainingHealth -= 1
            explosion = Explosion(self.rect.centerx, self.rect.centery, 1)
            explosionGroup.add(explosion)


# explosions
class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y, size):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        for num in range(1, 6):
            img = pygame.image.load(f"exp{num}.png")
            if size == 1:
                img = pygame.transform.scale(img, (20, 20))
            if size == 2:
                img = pygame.transform.scale(img, (40, 40))
            if size == 3:
                img = pygame.transform.scale(img, (160, 160))
            # add the image to the list
            self.images.append(img)
        self.index = 0
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.counter = 0


    def update(self):
        explosion_speed = 3
        # update explosion animation
        self.counter += 1

        if self.counter >= explosion_speed and self.index < len(self.images) - 1:
            self.counter = 0
            self.index += 1
            self.image = self.images[self.index]

        # if the animation is complete, delete explosion
        if self.index >= len(self.images) - 1 and self.counter >= explosion_speed:
            self.kill()


# sprite groups
spaceshipGroup = pygame.sprite.Group()
bulletGroup = pygame.sprite.Group()
alienGroup = pygame.sprite.Group()
alienBulletGroup = pygame.sprite.Group()
explosionGroup = pygame.sprite.Group()
shieldGroup = pygame.sprite.Group()

def create_shields():
    for i in range(8):
        shield = Shield(i * 100, screenHeight - 200)
        shieldGroup.add(shield)

def create_aliens():
    # generate aliens
    for row in range(rows):
        for item in range(columns):
            alien = Aliens(100 + item * 100, 100 + row * 70)
            alienGroup.add(alien)

create_aliens()
create_shields()

# player creation
spaceship = Spaceship(int(screenWidth / 2), screenHeight - 100, 3)
spaceshipGroup.add(spaceship)

run = True
while run:
    clock.tick(fps)

    # background
    draw_bg()


    if countdown == 0:
        # create random alien bullets
        # record current time
        timeNow = pygame.time.get_ticks()
        # shoot
        if timeNow - finalAlienShot > alien_cooldown and len(alienBulletGroup) < 5 and len(alienGroup) > 0:
            attacking_alien = random.choice(alienGroup.sprites())
            alien_bullet = Alien_Bullets(attacking_alien.rect.centerx, attacking_alien.rect.bottom)
            alienBulletGroup.add(alien_bullet)
            finalAlienShot = timeNow

        # if all aliens are dead
        if len(alienGroup) == 0:
            gameOver = 1

        if gameOver == 0:
            # update spaceship
            gameOver = spaceship.update()

            # update sprite groups
            bulletGroup.update()
            alienGroup.update()
            alienBulletGroup.update()
        else:
            if gameOver == -1:
                draw_text('GAME OVER!', fontBig, white, int(screenWidth / 2 - 100), int(screenHeight / 2 + 50))
            if gameOver == 1:
                draw_text('YOU WIN!', fontBig, white, int(screenWidth / 2 - 100), int(screenHeight / 2 + 50))

    if countdown > 0:
        draw_text('GET READY!', fontBig, white, int(screenWidth / 2 - 110), int(screenHeight / 2 + 50))
        draw_text(str(countdown), fontBig, white, int(screenWidth / 2 - 10), int(screenHeight / 2 + 100))
        count_timer = pygame.time.get_ticks()
        if count_timer - finalCount > 1000:
            countdown -= 1
            finalCount = count_timer


    # update explosion groups    
    explosionGroup.update()
    shieldGroup.update()

    # draw sprite groups
    spaceshipGroup.draw(screen)
    bulletGroup.draw(screen)
    alienGroup.draw(screen)
    alienBulletGroup.draw(screen)
    shieldGroup.draw(screen)
    explosionGroup.draw(screen)

    # event handlers
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False


    pygame.display.update()

pygame.quit()

