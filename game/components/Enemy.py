import pygame  
import random 
from pygame.sprite import Sprite  


class Enemi(Sprite):  
    def __init__(self, name, image, move_distance):  
        super().__init__()  
        self.name = name  
        self.move_distance = move_distance  
        self.image = pygame.transform.scale(image, (60, 60))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, pygame.display.get_surface().get_width() - self.rect.width)  # Establecer una posición x aleatoria dentro de los límites de la pantalla de juego
        self.rect.y = random.randint(0, pygame.display.get_surface().get_height() - self.rect.height)  # Establecer una posición y aleatoria dentro de los límites de la pantalla de juego
        self.speed_x = random.choice([-1, 1]) * random.randint(2, 5)  # Velocidad en el eje x (horizontal) con un factor aleatorio entre 2 y 5 dividido por 8
        self.speed_y = random.randint(2, 5)
        
    def update(self):
        self.rect.x += self.speed_x * self.move_distance
        self.rect.y += self.speed_y * self.move_distance

        # Si el enemigo sale completamente de la pantalla por la parte inferior,
        # lo volvemos a colocar en la parte superior de la pantalla con una nueva posición x aleatoria.
        if self.rect.y >= pygame.display.get_surface().get_height():
            self.rect.y = random.randint(-self.rect.height, 0)
            self.rect.x = random.randint(0, pygame.display.get_surface().get_width() - self.rect.width)

        # Rebotar en los lados de la pantalla
        if self.rect.left <= 0 or self.rect.right >= pygame.display.get_surface().get_width():
            self.speed_x *= -1

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        font = pygame.font.Font(None, 24)
        text = font.render(self.name, True, (255, 0, 0))
        text_rect = text.get_rect(center=(self.rect.x + self.rect.width // 2, self.rect.y + self.rect.height + 10))  # Obtener el rectángulo del texto y centrarlo debajo de la imagen del enemigo
        screen.blit(text, text_rect)  # Dibujar el texto en la pantalla

