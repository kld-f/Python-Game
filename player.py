import pygame

bottom = 300
img = pygame.image.load('images/player.png')

class Player:
    def __init__(self):
        self.x = 600
        self.y = 700
        self.vel_y = 5
        self.jump = False
        self.jump_height = 10
        self.running = False
        self.right = True
        self.direction = 0





