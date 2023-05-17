import pygame
import os

from pygame import surface
import buttons

pygame.init()
# creates the screen window
width = 1920
height = 1080
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('the shadow')

game_paused = False

TEXT_COL = (255, 255, 255)

# set framerate
clock = pygame.time.Clock()
FPS = 60

# define game variables
GRAVITY = 1
start_game = False

# define player action variables
left = False
right = False

# background loading and testing colors
BG = (144, 201, 120)
RED = (255, 0, 0)
background1 = pygame.image.load('images/1008526.jpg')
menu = pygame.image.load('images/menu.png')


# filling the screen with the background
def draw_bg():
    screen.fill(BG)
    pygame.draw.line(screen, RED, (100, 300), (width, 300))


# define fonts
play_img = pygame.image.load('images/menu/play.png').convert_alpha()
option_img = pygame.image.load('images/menu/options.png').convert_alpha()

# create button instances
start_button = buttons.Buttons(760, 200, play_img, 0.7)
option_button = buttons.Buttons(760, 600, option_img, 0.7)


# main class used so it can be used for both enemy and player

class Shadow(pygame.sprite.Sprite):
    def __init__(self, char_type, x, y, scale, speed):
        global temp_list
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        self.char_type = char_type
        self.speed = speed
        self.direction = 1
        self.vel_y = 0
        self.jump = False
        self.in_air = True
        self.attack = False
        self.health = 100
        self.max_health = self.health
        self.flip = False
        self.animation_list = []
        self.index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()

        # load all images for the players
        animation_types = ['idle', 'Run', 'jump', 'attack', 'death']
        for animation in animation_types:
            # cycle to every animation when called
            temp_list = []
            num_of_frames = len(os.listdir(f'images/{self.char_type}/{animation}'))
            for i in range(num_of_frames):
                img = pygame.image.load(f'images/{self.char_type}/{animation}/{i}.png').convert_alpha()
                self.image = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
                temp_list.append(img)
            self.animation_list.append(temp_list)

        self.animation_list.append(temp_list)
        self.image = self.animation_list[self.action][self.index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def move(self, move_left, move_right):
        # reset movement variables
        dx = 0
        dy = 0

        # put movement to left or right
        if move_left:
            dx = -self.speed
            self.flip = True
            self.direction = -1
        if move_right:
            dx = self.speed
            self.flip = False
            self.direction = 1

        # jump
        if self.jump == True and self.in_air == False:
            self.vel_y = -20
            self.jump = False
            self.in_air = True

        # apply gravity
        self.vel_y += GRAVITY
        if self.vel_y > 10:
            var = self.vel_y
        dy += self.vel_y

        # check collision with floor
        if self.rect.bottom + dy > 720:
            dy = 720 - self.rect.bottom
            self.in_air = False

        self.rect.x += dx
        self.rect.y += dy

    # how fast the animation cycle
    def update_animation(self):
        ANIMATION_COOLDOWN = 100

        self.image = self.animation_list[self.action][self.index]
        if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
            self.update_time = pygame.time.get_ticks()
            self.index += 1

        if self.index >= len(self.animation_list[self.action]):
            self.index = 0

    def update_action(self, new_action):
        # check if the new action is dfferent to the previous one
        if new_action != self.action:
            self.action = new_action
            self.index = 0
            self.update_time = pygame.time.get_ticks()

    def check_alive(self):
        if player.health <= 0:
            player.health = 0
            player.speed = 0
            self.alive = False
            self.update_action(4)

    def attack(self):
        attacking_rect = pygame.Rect(self.rect.centerx, self.rect.y * 2, self.rect.width, self.rect.height)
        pygame.draw.rect(surface, (255, 0, 0), self.rect)

    def draw(self):
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)


player = Shadow('player', 400, 700, 0.1, 10)
enemy = Shadow('enemy', 1100, 700, 1, 2)

# loads the player idle image
"img2 = pygame.transform.scale(img, (50, 90))"
background = pygame.image.load('images/1008526.png')  # loads the background
background1 = pygame.transform.scale(background1, (100, 3))

clock = pygame.time.Clock()

running = True
while running:


    clock.tick(FPS)

    if start_game == False:
        # main menu
        screen.fill(BG)
        # add buttons
        if start_button.draw(screen):
            start_game = True
        option_button.draw(screen)
    else:

        draw_bg()
        screen.blit(background, (0, 0))
        player.update_animation()
        player.draw()
        enemy.draw()
        enemy.update()
        enemy.update_animation()

        # update player actions
        if player.alive:
            if player.attack:
                player.update_action(3)
            elif player.in_air:
                player.update_action(2)
            elif left or right:
                player.update_action(1)
            else:
                player.update_action(0)

            player.move(left, right)
        user_input = pygame.key.get_pressed()

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                left = True
            if event.key == pygame.K_d:
                right = True
            if event.key == pygame.K_SPACE and player.alive:
                player.jump = True
            else:
                player.jump = False
            if event.key == pygame.K_f:
                player.attack = True
            else:
                player.attack = False
            if event.key == pygame.K_ESCAPE:
                running = False

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                left = False
            if event.key == pygame.K_d:
                right = False

    pygame.display.update()
    pygame.time.delay(20)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
