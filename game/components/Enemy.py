import pygame  
import random 
from pygame.sprite import Sprite  
from game.utils.constants import ENEMY_1, ENEMY_2 

class Enemys(Sprite):  
    def __init__(self, name, move_distance):  
        super().__init__()  
        self.name = name  
        self.move_distance = move_distance  

        if name == "dv1":  # Comprobar si el nombre es "dv1"
            image = ENEMY_1  # Asignar la imagen ENEMY_1 a la variable image
        elif name == "dv2":  # Comprobar si el nombre es "dv2"
            image = ENEMY_2  # Asignar la imagen ENEMY_2 a la variable image

        self.image = pygame.transform.scale(image, (60, 60))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, pygame.display.get_surface().get_width() - self.rect.width)  # Establecer una posición x aleatoria dentro de los límites de la pantalla de juego
        self.rect.y = random.randint(0, pygame.display.get_surface().get_height() - self.rect.height)  # Establecer una posición y aleatoria dentro de los límites de la pantalla de juego
        self.speed_x = random.choice([-1, 1]) * random.randint(2, 5) / 8.0  # Velocidad en el eje x (horizontal) con un factor aleatorio entre 2 y 5 dividido por 8
        self.speed_y = random.choice([-1, 1]) * random.randint(2, 5) / 8.0  # Velocidad en el eje y (vertical) con un factor aleatorio entre 2 y 5 dividido por 8

    def update(self):
        self.rect.x += self.speed_x * self.move_distance  # Actualizar la posición x del enemigo según la velocidad y la distancia de movimiento
        self.rect.y += self.speed_y * self.move_distance  # Actualizar la posición y del enemigo según la velocidad y la distancia de movimiento

        if self.rect.x <= 0 or self.rect.x >= pygame.display.get_surface().get_width() - self.rect.width:  # Comprobar si el enemigo ha alcanzado los límites de la pantalla en el eje x
            self.speed_x *= -1  # Invertir la dirección de la velocidad en el eje x

        if self.rect.y <= 0 or self.rect.y >= pygame.display.get_surface().get_height() - self.rect.height:  # Comprobar si el enemigo ha alcanzado los límites de la pantalla en el eje y
            self.speed_y *= -1  # Invertir la dirección de la velocidad en el eje y

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        font = pygame.font.Font(None, 24)
        text = font.render(self.name, True, (255, 0, 0))
        text_rect = text.get_rect(center=(self.rect.x + self.rect.width // 2, self.rect.y + self.rect.height + 10))  # Obtener el rectángulo del texto y centrarlo debajo de la imagen del enemigo
        screen.blit(text, text_rect)  # Dibujar el texto en la pantalla

