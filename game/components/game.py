import pygame
import random

# game.utils.constants -> es un modulo donde tengo "objetos" en memoria como el BG (background)...etc
#   tambien tenemos valores constantes como el title, etc
from game.utils.constants import BG, ICON, SCREEN_HEIGHT, SCREEN_WIDTH, TITLE, FPS, DEFAULT_TYPE, ENEMY_1, ENEMY_2
from game.components.spaceship import Ship
from game.components.enemy import Enemi
from pygame.sprite import Group

# Game es la definicion de la clase (plantilla o molde para sacar objetos)
# self es una referencia que indica que el metodo o el atributo es de cada "objeto" de la clase Game
class Game:
    def __init__(self):
        pygame.init() # este es el enlace con la libreria pygame para poder mostrar la pantalla del juego
        pygame.display.set_caption(TITLE)
        pygame.display.set_icon(ICON)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.playing = False
        self.game_speed = 10
        self.x_pos_bg = 0
        self.y_pos_bg = 0
        self.player = Ship(515,530, SCREEN_WIDTH, SCREEN_HEIGHT, "xwing") # Crea una instancia de la clase ship y le da la posicion deseada
        self.enemies = []
        self.enemy_speed = 1  # Establece la velocidad de los enemigos a 1.
        self.player_bullets = Group()  # Crea un grupo vacío para almacenar las balas del jugador.
        self.enemy_index = 1  # Inicializa un índice para llevar la cuenta de los enemigos creados.
        self.game_over = False  # Variable para controlar si la pantalla de "Game Over" debe mostrarse o no

    # este es el "game loop"
    # # Game loop: events - update - draw
    def run(self):
        self.playing = True 
        while self.playing:
            self.handle_events()
            self.update()
            self.check_collisions()  # Llamar al método para manejar colisiones con las balas del jugador
            self.draw()
            if self.game_over:
                self.wait_for_restart()
        pygame.display.quit()
        pygame.quit()

    def handle_events(self):
        # esta expression es la llamada a un metodo pygame.event.get() que devuelve un "iterable"
        for event in pygame.event.get(): # con el for sacamos cada evento del "iterable"
            if event.type == pygame.QUIT: # pygame.QUIT representa la X de la ventana
                self.playing = False
            
    #aca escribo ALGO de la logica "necesaria" -> repartimos responsabilidades entre clases
    # o sea aqui deberia llamar a los updates de mis otros objetos
    # si tienes un spaceship; el spaceship deberia tener un "update" method que llamamos desde aqui
    def update(self):
        user_input = pygame.key.get_pressed()  # Obtiene el estado del teclado.
        self.player.update(user_input)  # Actualiza el estado del jugador según la entrada del usuario.
        
        if len(self.enemies) < 10:  # Si hay menos de 10 enemigos en pantalla...
            self.create_enemy_at_top()  # ...crea un nuevo enemigo en la parte superior de la pantalla.

        # Actualiza cada enemigo en la lista de enemigos nuevamente, después de la posible adición de un nuevo enemigo.
        for enemy in self.enemies:
            enemy.update()

    def check_collisions(self):
        if not self.game_over:
            bullets_to_remove = []  # Lista para almacenar las balas que deben eliminarse.
            player_bullets = self.player.get_bullets()

    # Verificar colisiones entre la nave y los enemigos
            self.check_enemy_collisions()

    # Actualizar cada bala del jugador en la lista de balas del jugador.
            for bullet in player_bullets:
                bullet.update()
        # Verificar colisiones entre las balas del jugador y los enemigos.
                self.check_bullet_to_enemy_check_collisions(bullet, bullets_to_remove)
    # Eliminar las balas que colisionaron con enemigos.
            for bullet in bullets_to_remove:
                player_bullets.remove(bullet)

    # Crea un nuevo enemigo en la parte superior de la pantalla.
    def create_enemy_at_top(self):
        ENEMY_IMAGES = [ENEMY_1, ENEMY_2]  # Lista de imágenes de enemigos disponibles.
        image = random.choice(ENEMY_IMAGES)  # Elige una imagen de enemigo al azar.
        enemy = Enemi(f"dv{self.enemy_index}", image, self.enemy_speed)  # Crea una nueva instancia de Enemi (enemigo).
        self.enemy_index += 1  # Incrementa el índice de enemigos.
        enemy.rect.x = random.randint(0, SCREEN_WIDTH - enemy.rect.width)  # Posiciona el enemigo en una coordenada X aleatoria.
        enemy.rect.y = -enemy.rect.height  # Posiciona el enemigo fuera de la pantalla en la coordenada Y.
        self.enemies.append(enemy)  # Agrega el nuevo enemigo a la lista de enemigos del juego.


    # este metodo "dibuja o renderiza o refresca mis cambios en la pantalla del juego"
    # aca escribo ALGO de la logica "necesaria" -> repartimos responsabilidades entre clases
    # o sea aqui deberia llamar a los metodos "draw" de mis otros objetos
    # si tienes un spaceship; el spaceship deberia tener un "draw" method que llamamos desde aqui
    def draw(self):
        self.clock.tick(FPS) # configuramos cuantos frames dibujaremos por segundo
        self.screen.fill((255, 255, 255)) # esta tupla (255, 255, 255) representa un codigo de color: blanco
        self.draw_background()
        self.player.draw(self.screen)
        for enemy in self.enemies:
            enemy.draw(self.screen)
        
        for bullet in self.player.get_bullets():
            bullet.draw(self.screen)
        pygame.display.update()


    # Mostrar pantalla de "Game Over" si el jugador se queda sin vidas
        if self.player.lives <= 0:
            self.game_over_screen()

    def draw_background(self):
        # le indicamos a pygame que transforme el objeto BG (que es una imagen en memoria, no es un archivo)
        # y le pedimos que ajuste el ancho y alto de esa imagen
        image = pygame.transform.scale(BG, (SCREEN_WIDTH, SCREEN_HEIGHT))
        # obtenemos el alto de la imagen
        image_height = image.get_height()
        ## DIBUJAMOS dos veces para dar la impresion de que nos movemos en el spacio
        # blit DIBUJA la imagen en memoria en una posicion (x, y)
        self.screen.blit(image, (self.x_pos_bg, self.y_pos_bg))
        # blit DIBUJA la imagen en memoria en una posicion (x, y)
        self.screen.blit(image, (self.x_pos_bg, self.y_pos_bg - image_height))
        # Controlamos que en el eje Y (vertical) si me sali del screen height (alto de pantalla)
        if self.y_pos_bg >= SCREEN_HEIGHT:
            # dibujo la imagen
            self.screen.blit(image, (self.x_pos_bg, self.y_pos_bg - image_height))
            # reseteo la posicion en y
            self.y_pos_bg = 0
        # No hay una velocidad de juego como tal, el "game_speed" simplemente me indica
        # cuanto me voy a mover (cuantos pixeles hacia arriba o abajo) cen el eje Y
        self.y_pos_bg += self.game_speed

    def game_over_screen(self):
        self.screen.fill((0, 0, 0))  # Rellenar la pantalla con color negro
        font = pygame.font.Font(None, 36)
        text = font.render("Game Over", True, (255, 0, 0))
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(text, text_rect)

        font = pygame.font.Font(None, 24)
        player_name_text = font.render(f"Player Name: {self.player.name}", True, (255, 255, 255))
        destroyed_enemies_text = font.render(f"Enemies Destroyed: {self.player.count}", True, (255, 255, 255))

        name_text_rect = player_name_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 40))
        destroyed_enemies_rect = destroyed_enemies_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 80))

        self.screen.blit(player_name_text, name_text_rect)
        self.screen.blit(destroyed_enemies_text, destroyed_enemies_rect)

        pygame.display.flip()

        # Esperar hasta que el usuario presione cualquier botón
        self.wait_for_restart()

    def wait_for_restart(self):
        # Método para esperar la entrada del jugador para reiniciar después de Game Over.
        waiting_for_restart = True
        while waiting_for_restart:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN or event.type == pygame.QUIT:
                    waiting_for_restart = False
                    self.reset()  # Reiniciar el juego completo
                    
    def reset(self):
        # Reiniciar los valores del juego.
        self.player.reset()
        self.enemies.clear()
        self.player_bullets.empty()
        self.enemy_index = 1
        self.game_over = False

    def check_enemy_collisions(self):
        for enemy in self.enemies:
            if self.player.rect.colliderect(enemy.rect):
                self.player.lose_life()  # Restar una vida al jugador
                self.enemies.remove(enemy)  # Eliminar el enemigo que colisionó con la nave

                if self.player.lives <= 0:
                    self.game_over_screen()  # Mostrar pantalla de "Game Over" si el jugador se queda sin vidas
                    self.game_over = True  # Finalizar el juego
    
    def check_bullet_to_enemy_check_collisions(self, bullet, bullets_to_remove):
        for enemy in self.enemies:
            if bullet.rect.colliderect(enemy.rect):
                bullets_to_remove.append(bullet)  # Agregar la bala a la lista de balas a eliminar.
                self.enemies.remove(enemy)  # Eliminar el enemigo que colisionó con la bala del jugador.
                self.player.increase_count()  # Incrementar el contador de enemigos eliminados por el jugador.