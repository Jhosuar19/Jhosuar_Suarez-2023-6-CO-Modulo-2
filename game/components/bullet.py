import pygame
from pygame.sprite import Sprite
from game.utils.constants import BULLET

class Bullet(Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.transform.scale(BULLET, (10, 30))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = -10  # Velocidad hacia arriba (negativa en el eje y)

    def update(self):
        self.rect.y += self.speed

    def draw(self, screen):
        screen.blit(self.image, self.rect)