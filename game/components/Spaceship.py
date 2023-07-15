import pygame
from pygame.sprite import Sprite
from game.utils.constants import SPACESHIP

class Ship(Sprite):
    def __init__(self, x, y, screen_width, screen_height,name):
        super().__init__()
        self.original_image = SPACESHIP  # Imagen original de la nave
        self.image = pygame.transform.scale(self.original_image, (60, 60))  # Redimensionar la imagen a 60x60 píxeles
        self.rect = self.image.get_rect()  # Obtener el rectángulo de la imagen
        self.rect.x = x  # Posición inicial en el eje x
        self.rect.y = y  # Posición inicial en el eje y
        self.ship_speed = 10  # Velocidad de la nave
        self.screen_width = screen_width  # Ancho de la pantalla
        self.screen_height = screen_height  # Alto de la pantalla
        self.name = name 

    def update(self, user_input):
        # Actualizar la posición de la nave 
        self.rect.y += (user_input[pygame.K_DOWN] - user_input[pygame.K_UP]) * self.ship_speed
        self.rect.x += (user_input[pygame.K_RIGHT] - user_input[pygame.K_LEFT]) * self.ship_speed
        # Limitar la posición de la nave para que no se salga de la pantalla
        self.rect.x = max(0, min(self.rect.x, self.screen_width - self.rect.width))
        self.rect.y = max(0, min(self.rect.y, self.screen_height - self.rect.height))

    def draw(self, screen):
        # Dibujar la nave en la pantalla en su posición actual
        screen.blit(self.image, (self.rect.x, self.rect.y))
        # Mostrar el nombre de la nave como un label
        font = pygame.font.Font(None, 24)
        text = font.render(self.name, True, (255, 255, 255))
        text_rect = text.get_rect(center=(self.rect.x + self.rect.width // 2, self.rect.y + self.rect.height - 65))
        screen.blit(text, text_rect)