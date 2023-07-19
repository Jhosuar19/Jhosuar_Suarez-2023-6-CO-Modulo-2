import pygame
from pygame.sprite import Sprite
from game.utils.constants import SPACESHIP, HEART
from game.components.bullet import Bullet

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
        self.name = name # Nombre nave 
        self.count = 0
        self.player_bullets = pygame.sprite.Group()  # Usamos el sprite.Group de pygame
        self.can_shoot = True  # Propiedad para controlar si el jugador puede disparar
        self.lives = 10  # Número de vidas iniciales del jugador

    def update(self, user_input):
        # Actualizar la posición de la nave 
        self.rect.y += (user_input[pygame.K_DOWN] - user_input[pygame.K_UP]) * self.ship_speed
        self.rect.x += (user_input[pygame.K_RIGHT] - user_input[pygame.K_LEFT]) * self.ship_speed
        # Limitar la posición de la nave para que no se salga de la pantalla
        self.rect.x = max(0, min(self.rect.x, self.screen_width - self.rect.width))
        self.rect.y = max(0, min(self.rect.y, self.screen_height - self.rect.height))

        if user_input[pygame.K_SPACE] and self.can_shoot:
            self.shoot()
            self.can_shoot = False  # Desactivamos el disparo para evitar ráfagas continuas
        elif not user_input[pygame.K_SPACE]:
            self.can_shoot = True  # Restauramos la capacidad de disparar cuando se suelta la tecla

    def increase_count(self):
        self.count += 1

    def draw(self, screen):
        # Dibujar la nave en la pantalla en su posición actual
        screen.blit(self.image, (self.rect.x, self.rect.y))
        # Mostrar el nombre de la nave como un label
        font = pygame.font.Font(None, 24)
        text = font.render(self.name, True, (255, 255, 255))
        text_rect = text.get_rect(center=(self.rect.x + self.rect.width // 2, self.rect.y + self.rect.height - 80))
        screen.blit(text, text_rect)
        # Mostrar el contador de enemigos destruidos debajo del nombre de la nave
        counter_text = font.render(f"Enemies Destroyed: {self.count}", True, (255, 0, 0))
        counter_text_rect = counter_text.get_rect(center=(self.rect.x + self.rect.width // 2, self.rect.y + self.rect.height -65))
        screen.blit(counter_text, counter_text_rect)
        heart_x = 10  # Posición horizontal del primer corazón
        heart_y = 10  # Posición vertical del primer corazón
        for _ in range(self.lives):
            screen.blit(HEART, (heart_x, heart_y))
            heart_x += HEART.get_width() + 5

    def shoot(self):
        bullet = Bullet(self.rect.x + self.rect.width // 2, self.rect.y)
        self.player_bullets.add(bullet)  # Agregamos la bala al sprite.Group de balas del jugador

    def get_bullets(self):
        return self.player_bullets
    

    def lose_life(self):
        if self.lives > 0:
            self.lives -= 1

    def reset(self):
        self.rect.x = 515
        self.rect.y = 530
        self.count = 0
        self.lives = 10
        self.player_bullets.empty()
        self.can_shoot = True
