import pygame
import math
import random

# ---- Config ----
WHITE = (245, 245, 245)
GREEN = (50, 155, 50)
DARK_GREEN = (32, 120, 32)
BLUE = (40, 130, 230)
RED = (220, 60, 60)
YELLOW = (240, 220, 60)
BLACK = (20, 20 , 20)
GRAY  = (200, 200, 200)

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
        self.color =color
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