# juego_futbolin_python
# ⚽ Juego de Fútbol en Python con Pygame

Este es un juego sencillo de fútbol hecho en **Python** usando la librería **Pygame**.  
Controlas a un jugador, puedes moverlo, chutar el balón y jugar contra otro jugador en el mismo teclado.  
El juego está hecho con **formas geométricas (círculos/rectángulos)**, por lo que no necesita imágenes externas.

---

## 🚀 Requisitos

- Python **3.8+**
- Instalar Pygame:

```bash
pip install pygame

📄 Archivo principal
python

"""
futbol.py
Juego de fútbol simple en Python con Pygame.
Controles:
  Jugador 1 (equipo azul): W A S D para moverse, F para chutar
  Jugador 2 (equipo rojo): Flechas para moverse, RCTRL (Right Ctrl) para chutar

Objetivo: llevar la pelota a la portería contraria.
"""

import pygame
import math
import random

# ---- Config ----
WIDTH, HEIGHT = 900, 600
FPS = 60
PLAYER_RADIUS = 18
BALL_RADIUS = 10
PLAYER_SPEED = 4.0
KICK_POWER = 8.5
FRICTION = 0.99
GOAL_WIDTH = 140
SCORE_TO_WIN = 5

# Colores
WHITE = (245, 245, 245)
GREEN = (50, 155, 50)
DARK_GREEN = (32, 120, 32)
BLUE = (40, 130, 230)
RED = (220, 60, 60)
YELLOW = (240, 220, 60)
BLACK = (20, 20, 20)
GRAY = (200, 200, 200)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Fútbol simple - Pygame")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)
big_font = pygame.font.SysFont(None, 72)

# ---- Utilidades ----
def clamp(n, a, b):
    return max(a, min(b, n))

def distance(a, b):
    return math.hypot(a[0] - b[0], a[1] - b[1])

# ---- Clases ----
class Player:
    def __init__(self, x, y, color, up_key, left_key, down_key, right_key, kick_key):
        self.x = x
        self.y = y
        self.color = color
        self.vx = 0
        self.vy = 0
        self.score = 0
        self.keys = {
            "up": up_key,
            "left": left_key,
            "down": down_key,
            "right": right_key,
            "kick": kick_key
        }

    def handle_input(self, keys_pressed):
        dx = dy = 0
        if keys_pressed[self.keys["up"]]:
            dy -= 1
        if keys_pressed[self.keys["down"]]:
            dy += 1
        if keys_pressed[self.keys["left"]]:
            dx -= 1
        if keys_pressed[self.keys["right"]]:
            dx += 1

        if dx != 0 or dy != 0:
            length = math.hypot(dx, dy)
            self.vx = (dx / length) * PLAYER_SPEED
            self.vy = (dy / length) * PLAYER_SPEED
        else:
            self.vx *= 0.85
            self.vy *= 0.85

        self.x += self.vx
        self.y += self.vy

        # Mantener en el campo
        margin = PLAYER_RADIUS + 4
        self.x = clamp(self.x, margin, WIDTH - margin)
        self.y = clamp(self.y, margin, HEIGHT - margin)

    def draw(self, surf):
        pygame.draw.circle(surf, self.color, (int(self.x), int(self.y)), PLAYER_RADIUS)
        # borde
        pygame.draw.circle(surf, BLACK, (int(self.x), int(self.y)), PLAYER_RADIUS, 2)

class Ball:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vx = 0.0
        self.vy = 0.0

    def update(self):
        # aplicar velocidad
        self.x += self.vx
        self.y += self.vy
        # fricción
        self.vx *= FRICTION
        self.vy *= FRICTION
        # choque con paredes (rebote en top/bottom)
        if self.y - BALL_RADIUS <= 0 and self.vy < 0:
            self.y = BALL_RADIUS
            self.vy *= -0.6
        if self.y + BALL_RADIUS >= HEIGHT and self.vy > 0:
            self.y = HEIGHT - BALL_RADIUS
            self.vy *= -0.6
        # limitar dentro X (para evitar perderla fuera del canvas)
        self.x = clamp(self.x, -100, WIDTH + 100)

    def draw(self, surf):
        pygame.draw.circle(surf, WHITE, (int(self.x), int(self.y)), BALL_RADIUS)
        pygame.draw.circle(surf, BLACK, (int(self.x), int(self.y)), BALL_RADIUS, 2)

# ---- Funciones de juego ----
def reset_positions(players, ball):
    players[0].x, players[0].y = WIDTH * 0.2, HEIGHT / 2
    players[0].vx = players[0].vy = 0
    players[1].x, players[1].y = WIDTH * 0.8, HEIGHT / 2
    players[1].vx = players[1].vy = 0
    ball.x, ball.y = WIDTH / 2, HEIGHT / 2
    ball.vx = ball.vy = 0

def check_player_ball_collision(player, ball, kick_pressed=False):
    dist = distance((player.x, player.y), (ball.x, ball.y))
    if dist <= PLAYER_RADIUS + BALL_RADIUS:
        # empujar la pelota en dirección del jugador
        dx = ball.x - player.x
        dy = ball.y - player.y
        if dx == 0 and dy == 0:
            dx = random.uniform(-0.5, 0.5)
            dy = random.uniform(-0.5, 0.5)
        length = math.hypot(dx, dy)
        nx, ny = dx / length, dy / length
        # si el jugador está chutando y cerca, aplicar mayor fuerza
        power = KICK_POWER if kick_pressed else 1.6
        ball.vx = nx * power + player.vx * 0.6
        ball.vy = ny * power + player.vy * 0.6
        # separar para evitar quedar pegados
        overlap = (PLAYER_RADIUS + BALL_RADIUS) - dist + 1
        ball.x += nx * overlap
        ball.y += ny * overlap

def draw_field(surf):
    surf.fill(DARK_GREEN)
    pygame.draw.rect(surf, GREEN, (40, 40, WIDTH - 80, HEIGHT - 80))
    # líneas del campo
    pygame.draw.rect(surf, WHITE, (40, 40, WIDTH - 80, HEIGHT - 80), 4)
    # línea central

▶️ Ejecutar el juego
En la terminal, dentro de la carpeta donde guardaste futbol.py, ejecuta:
bash  
python futbol.py
