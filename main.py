import pygame
import time
import random

from sorts import *
from data import *

pygame.init()

WIDTH, HEIGHT = 800, 600
FPS = 60

display = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

def menu():
    pass

def sorting(method):
    n = 200
    values = [int((x / n) * WIDTH) for x in range(n)]
    random.shuffle(values)
    data = Data(values)
    data.delay = 0.01
    thread = perform(method, data)

    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                quit()
        
        data.draw(display, 0, 0, WIDTH, HEIGHT)

        pygame.display.update()

if __name__ == "__main__":
    sorting("merge_sort")



    


