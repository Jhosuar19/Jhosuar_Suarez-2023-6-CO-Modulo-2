import pygame
from pygame.sprite import Sprite
from game.utils.constants import BULLET

class Bullet(Sprite):
    def __init__(self, x, y):
        super().__init__()

        # Crea una bala con una imagen escalada y una posición inicial (x, y).
        self.image = pygame.transform.scale(BULLET, (10, 30))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = 10  # Velocidad hacia arriba (negativa en el eje y)

    def update(self):
        # Actualiza la posición de la bala moviéndola hacia arriba según su velocidad.
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()

    def draw(self, screen):
        # Dibuja la bala en la pantalla en su posición actual (rectángulo que la rodea).
        screen.blit(self.image, self.rect)
