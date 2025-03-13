import pygame
import sys

# Inicializar Pygame
pygame.init()

# Configuraciones de la pantalla
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Brick Breaker")

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Reloj para controlar FPS
clock = pygame.time.Clock()
FPS = 60

# Variables globales
lives = 3
score = 0  # Variable global para la puntuación

# Posiciones iniciales
paddle_x = WIDTH // 2 - 50
paddle_y = HEIGHT - 30
ball_x, ball_y = WIDTH // 2, HEIGHT // 2
ball_dx, ball_dy = 4, -4

# Crear ladrillos
bricks = []
for row in range(5):
    for col in range(10):
        brick_x = col * (75 + 5) + 35
        brick_y = row * (20 + 5) + 50
        bricks.append(pygame.Rect(brick_x, brick_y, 75, 20))

# Funciones personalizadas
def draw_text(text, font_size, color, x, y):
    """Dibuja texto en la pantalla."""
    font = pygame.font.Font(None, font_size)
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))

def show_menu():
    """Muestra el menú principal."""
    global score  # Reiniciar la puntuación al iniciar el juego
    score = 0
    while True:
        screen.fill(BLACK)
        draw_text("Brick Breaker", 74, WHITE, WIDTH // 2 - 200, HEIGHT // 4)
        draw_text("Presiona ESPACIO para jugar", 36, GREEN, WIDTH // 2 - 200, HEIGHT // 2)
        draw_text("Presiona ESC para salir", 36, RED, WIDTH // 2 - 200, HEIGHT // 2 + 50)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        pygame.display.flip()

def game_over_screen(final_score):
    """Muestra la pantalla de 'Game Over'."""
    while True:
        screen.fill(BLACK)
        draw_text("GAME OVER", 74, RED, WIDTH // 2 - 150, HEIGHT // 4)
        draw_text(f"Puntuación Final: {final_score}", 36, WHITE, WIDTH // 2 - 150, HEIGHT // 2)
        draw_text("Presiona R para reiniciar", 36, GREEN, WIDTH // 2 - 150, HEIGHT // 2 + 50)
        draw_text("Presiona ESC para salir", 36, RED, WIDTH // 2 - 150, HEIGHT // 2 + 100)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # Reiniciar el juego
                    return True
                if event.key == pygame.K_ESCAPE:  # Salir del juego
                    pygame.quit()
                    sys.exit()

        pygame.display.flip()

# Clase Game
class Game:
    def __init__(self):
        global score  # Usar la variable global `score`
        self.paddle_x = WIDTH // 2 - 50
        self.paddle_y = HEIGHT - 30
        self.ball_x, self.ball_y = WIDTH // 2, HEIGHT // 2
        self.ball_dx, self.ball_dy = 4, -4
        self.lives = 3
        self.score = score  # Inicializar con el valor global de `score`
        self.running = True

    def run(self):
        global bricks, score  # Usar las variables globales
        while self.running:
            screen.fill(BLACK)

            # Eventos
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            # Movimiento de la paleta
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and self.paddle_x > 0:
                self.paddle_x -= 5
            if keys[pygame.K_RIGHT] and self.paddle_x < WIDTH - 100:
                self.paddle_x += 5

            # Actualizar posición de la pelota
            self.ball_x += self.ball_dx
            self.ball_y += self.ball_dy

            # Rebotar en los bordes
            if self.ball_x <= 0 or self.ball_x >= WIDTH:
                self.ball_dx = -self.ball_dx
            if self.ball_y <= 0:
                self.ball_dy = -self.ball_dy

            # Colisión con la paleta
            if (self.paddle_x < self.ball_x < self.paddle_x + 100 and
                self.paddle_y < self.ball_y < self.paddle_y + 10):
                self.ball_dy = -self.ball_dy

            # Colisión con los ladrillos
            for brick in bricks[:]:
                if brick.collidepoint(self.ball_x, self.ball_y):
                    bricks.remove(brick)
                    self.ball_dy = -self.ball_dy
                    self.score += 10  # Incrementar la puntuación
                    score = self.score  # Actualizar la variable global
                    break

            # Pelota cae al suelo
            if self.ball_y > HEIGHT:
                self.lives -= 1
                self.ball_x, self.ball_y = WIDTH // 2, HEIGHT // 2
                self.ball_dx, self.ball_dy = 4, -4
                if self.lives == 0:
                    self.running = False
                    if game_over_screen(score):  # Pasar la puntuación final
                        self.__init__()  # Reinicia el juego
                        bricks.clear()  # Limpia los ladrillos anteriores
                        for row in range(5):
                            for col in range(10):
                                brick_x = col * (75 + 5) + 35
                                brick_y = row * (20 + 5) + 50
                                bricks.append(pygame.Rect(brick_x, brick_y, 75, 20))
                        self.run()  # Vuelve a ejecutar el juego

            # Dibujar elementos
            pygame.draw.rect(screen, WHITE, (self.paddle_x, self.paddle_y, 100, 10))  # Paleta
            pygame.draw.circle(screen, WHITE, (self.ball_x, self.ball_y), 8)          # Pelota
            for brick in bricks:
                pygame.draw.rect(screen, RED, brick)                                   # Ladrillos

            # Mostrar puntuación y vidas
            draw_text(f"Puntuación: {self.score}", 36, WHITE, 10, 10)
            draw_text(f"Vidas: {self.lives}", 36, WHITE, WIDTH - 150, 10)

            pygame.display.flip()
            clock.tick(FPS)

        pygame.quit()

# Función principal
def main():
    show_menu()
    game = Game()
    game.run()

if __name__ == "__main__":
    main()
