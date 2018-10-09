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

class Button:
    def __init__(self, text, x, y, width, height, func, args):
        self.text = text
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.func = func
        self.args = args

    def handle(self, e):
        if e.type == pygame.MOUSEBUTTONUP:
            x, y = e.pos
            if x >= self.x and x < self.x + self.width:
                if y >= self.y and y < self.y + self.height:
                    self.func(*self.args)

    def get_rect(self):
        return (self.x, self.y, self.width, self.height)
    
    def draw(self, surface):
        font = pygame.font.SysFont("Consolas", self.height // 2)
        pygame.draw.rect(surface, (255, 255, 255), self.get_rect())
        rendered = font.render(self.text, 1, (0, 0, 0))
        surface.blit(rendered, ((self.x + self.width // 2) - rendered.get_width() // 2,
                                (self.y + self.height // 2) - rendered.get_height() // 2))

def menu():
    buttons = []
    button_height = 30
    button_width = 200
    padding = 10
    x = padding
    y = padding
    for sort in sorts:
        buttons.append(Button(sort, x, y, button_width, button_height, func=sorting, args=(sort,)))
        y += button_height + padding
    
    while True:

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                quit()
                
            for button in buttons:
                button.handle(e)

        display.fill((0, 0, 0))
        
        for button in buttons:
            button.draw(display)

        pygame.display.update()
        clock.tick(FPS)
        

def sorting(method):
    n = 200
    values = [int((x / n) * WIDTH) for x in range(n)]
    random.shuffle(values)
    data = Data(values)
    data.delay = 0.01
    thread = perform(method, data)

    while thread.isAlive():
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                quit()
                
            elif e.type == pygame.KEYUP:
                if e.key == pygame.K_ESCAPE:
                    data.delay = 0
        
        data.draw(display, 0, 0, WIDTH, HEIGHT)

        pygame.display.update()

if __name__ == "__main__":
    menu()



    


