import pygame
import random
import math

# Inicializar Pygame
pygame.init()

# Configuración de la pantalla
width, height = 600, 400
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Adrian Martinez Martinez - Virus Simulator")

# Colores
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)

class Virus:
    def __init__(self, x, y, color=RED):
        self.x = x
        self.y = y
        self.radius = 30
        self.speed = 8
        self.direction = random.uniform(0, 2 * math.pi)
        self.reproduction_cooldown = 0
        self.color = color
        self.outline = False
        self.outline_timer = 0

    def move(self):
        self.x += self.speed * math.cos(self.direction)
        self.y += self.speed * math.sin(self.direction)
        
        # Rebotar en los bordes
        if self.x < 0 or self.x > width:
            self.direction = math.pi - self.direction
        if self.y < 0 or self.y > height:
            self.direction = -self.direction

        # Reducir el tiempo de espera para la reproducción
        if self.reproduction_cooldown > 0:
            self.reproduction_cooldown -= 1

        # Manejar el temporizador del contorno
        if self.outline_timer > 0:
            self.outline_timer -= 1
        else:
            self.outline = False

    def draw(self):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)
        if self.outline:
            pygame.draw.circle(screen, WHITE, (int(self.x), int(self.y)), self.radius + 2, 1)

    def reproduce(self):
        self.reproduction_cooldown = 300
        self.outline = True
        self.outline_timer = 180  # 3 segundos a 60 FPS

# Inicializar la lista con solo dos virus
viruses = [
    Virus(random.randint(0, width), random.randint(0, height)),
    Virus(random.randint(0, width), random.randint(0, height))
]

# Inicializar la fuente para el contador
font = pygame.font.Font(None, 36)

# Bucle principal
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(BLACK)

    # Mover y dibujar virus
    for virus in viruses:
        virus.move()
        virus.draw()

    # Comprobar colisiones y reproducción
    for i, virus1 in enumerate(viruses):
        for j, virus2 in enumerate(viruses[i+1:], start=i+1):
            distance = math.hypot(virus1.x - virus2.x, virus1.y - virus2.y)
            if distance < virus1.radius + virus2.radius:
                # Solo reproducir si ambos virus no están en tiempo de espera y no hemos alcanzado el límite
                if virus1.reproduction_cooldown == 0 and virus2.reproduction_cooldown == 0 and len(viruses) < 20:
                    # Crear un nuevo virus en una posición cercana
                    new_x = (virus1.x + virus2.x) / 2 + random.randint(-10, 10)
                    new_y = (virus1.y + virus2.y) / 2 + random.randint(-10, 10)
                    new_virus = Virus(new_x, new_y, BLUE)  # Nueva bolita de color azul
                    viruses.append(new_virus)
                    
                    # Activar la reproducción en los virus padres
                    virus1.reproduce()
                    virus2.reproduce()
                    break  # Solo permitir una reproducción por ciclo

    # Mostrar el contador de virus
    counter_text = font.render(f"Virus: {len(viruses)}/20", True, WHITE)
    screen.blit(counter_text, (10, 10))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()