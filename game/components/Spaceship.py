import pygame
from pygame.sprite import Sprite
from game.utils.constants import SPACESHIP

class Ship(Sprite):
    def __init__(self, x, y, screen_width, screen_height):
        super().__init__()
        self.original_image = SPACESHIP[0]
        self.image = pygame.transform.scale(self.original_image, (60, 60))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.ship_speed = 10
        self.screen_width = screen_width
        self.screen_height = screen_height

    def update(self, user_input):
        self.rect.x += (user_input[pygame.K_RIGHT] - user_input[pygame.K_LEFT]) * self.ship_speed
        self.rect.x = max(0, min(self.rect.x, self.screen_width - self.rect.width))

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))