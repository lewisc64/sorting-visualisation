import pygame
import threading
import time
import random

def bubble_sort(data):
    for i in range(len(data) - 1, 1, -1):
        
        flag = False
        for j in range(i):
            
            if data[j] > data[j + 1]:
                flag = True

                
                data.active_positions = [j, j + 1]
                data.wait_for_step()
                
                data[j], data[j + 1] = data[j + 1], data[j]
            
        data.sorted_positions.append(i)

        if not flag:
            break

def merge_sort(data, i=None, j=None):
    if i is None:
        i = 0
    if j is None:
        j = len(data) - 1

    
    
    if i == j:
        return i, j

    i1, j1 = merge_sort(data, i, (i + j) // 2)
    i2, j2 = merge_sort(data, (i + j) // 2 + 1, j)
    
    data.active_positions = [x for x in range(i, j+1)]
    
    merge(data, i1, j1, i2, j2)
    return i, j

def merge(data, i1, j1, i2, j2):
    i = i1
    a1 = data[i1:j1+1]
    a2 = data[i2:j2+1]
    i1 = 0
    i2 = 0
    while i1 < len(a1) or i2 < len(a2):
        data.wait_for_step()
        if i1 >= len(a1):
            data[i] = a2[i2]
            i2 += 1
        elif i2 >= len(a2):
            data[i] = a1[i1]
            i1 += 1
        elif a1[i1] > a2[i2]:
            data[i] = a2[i2]
            i2 += 1
        else:
            data[i] = a1[i1]
            i1 += 1
        i += 1
            

def perform(func, data):
    thread = threading.Thread(target=func, args=(data,))
    thread.start()

class Data:
    def __init__(self, values):
        self.values = values
        self.maximum = max(self.values)
        self.sorted_positions = []
        self.active_positions = []
        self.do_step = False
        self.list_accesses = 0
        self.list_assignments = 0

    def __iter__(self):
        return (x for x in self.values)

    def __len__(self):
        return len(self.values)
    
    def __getitem__(self, key):
        if isinstance(key, slice):
            return self.values[key.start:key.stop:key.step]
        else:
            self.list_accesses += 1
            return self.values[key]

    def __setitem__(self, i, v):
        self.list_assignments += 1
        self.values[i] = v
    
    def step(self):
        self.do_step = True
    
    def wait_for_step(self):
        while not self.do_step:
            pass
        self.do_step = False

    def draw(self, surface, x, y, width, height):
        
        bar_width = max(int(width / len(self.values)), 1)
        for i in range(len(self.values)):
            bar_x = x + width * (i / len(self.values))
            bar_height = height * (self.values[i] / self.maximum)

            color = (255, 255, 255)
            if i in self.sorted_positions:
                color = (0, 255, 0)
            if i in self.active_positions:
                color = (255, 0, 255)

            pygame.draw.rect(surface, color, (bar_x, y + (height - bar_height), bar_width, bar_height))

if __name__ == "__main__":

    pygame.init()
    WIDTH, HEIGHT = 800, 600
    FPS = 60
    display = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    cooldown_amount = 1
    cooldown = cooldown_amount

    data = Data([random.randint(1, 600) for x in range(100)])

    perform(merge_sort, data)

    while True:

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif e.type == pygame.KEYUP:
                if e.key == pygame.K_SPACE:
                    data.step()

        cooldown -= 1
        if cooldown <= 0:
            cooldown = cooldown_amount
            data.step()
        
        display.fill((0, 0, 0))
        data.draw(display, 0, 0, WIDTH, HEIGHT)

        pygame.display.update()
        #clock.tick(FPS)
