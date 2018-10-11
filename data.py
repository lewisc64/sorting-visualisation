import threading
import pygame
import time
import math
import struct

import pyaudio
p = pyaudio.PyAudio()
audio_device_index = p.get_default_output_device_info()["index"]
sample_rate = 44100
chunk_size = 1024

def audio_function(n, f):
    return int(math.sin(n * 2 * math.pi * f / sample_rate) * 8000)
    #return (1 if ((n % (sample_rate / f9*)) * (f / sample_rate) * 2 - 1) > 0 else -1) * 8000
    #return int(((n % (sample_rate / f)) * (f / sample_rate) * 2 - 1) * 8000)

def audio_loop(data, thread):
    
    stream = p.open(format=p.get_format_from_width(2),
                    channels=1,
                    rate=sample_rate,
                    output_device_index=audio_device_index,
                    output=True)
    
    n = 0
    
    while thread.isAlive():
        
        sample_chunk = []
        
        f = data.frequency
        
        for x in range(chunk_size):
            sample_chunk.append(audio_function(n, f))
            n += 1
        
        bytes = struct.pack("<{}{}".format(len(sample_chunk), "h"), *sample_chunk)
        stream.write(bytes)
            
    stream.stop_stream()
    stream.close()
    
def play_audio(data, sort_thread):
    thread = threading.Thread(target=audio_loop, args=(data, sort_thread))
    thread.start()
    return thread

class Data:
    def __init__(self, values=None):
        if values is None:
            self.values = []
            self.maximum = 0
        else:
            self.values = values
            self.maximum = max(self.values)
            
        self.sorted_positions = []
        self.active_positions = []
        self.dirty = set([x for x in range(len(values))])
        
        self.list_accesses = 0
        self.list_assignments = 0

        self.step_through = False
        self.do_step = False
        self.delay = 0
        self.frequency = 440

    def set_active_positions(self, positions):
        self.dirty.update(positions)
        self.dirty.update(self.active_positions)
        self.active_positions = positions
    
    def __iter__(self):
        return (x for x in self.values)

    def __len__(self):
        return len(self.values)
    
    def __getitem__(self, key):
        if isinstance(key, slice):
            return self.values[key.start:key.stop:key.step]
        else:
            self.frequency = 440 + 440 * (self.values[key] / self.maximum)
            self.list_accesses += 1
            return self.values[key]

    def __setitem__(self, i, v):
        self.dirty.add(i)
        self.list_assignments += 1
        self.values[i] = v
        self.frequency = 440 + 440 * (self.values[i] / self.maximum)
        
    
    def step(self):
        self.do_step = True
    
    def wait_for_step(self):
        while self.step_through and not self.do_step:
            pass
        if self.delay > 0:
            t = time.time()
            while time.time() - t < self.delay:
                pass
        self.do_step = False

    def get_color(self, i):
        if i in self.sorted_positions:
            return (0, 255, 0)
        if i in self.active_positions:
            return (255, 0, 255)
        return (255, 255, 255)

    def draw(self, surface, x, y, width, height):
        
        if self.dirty:
            bar_width = max(int(width / len(self.values)), 1)
            bar_x = 0
            for i in range(len(self.values)):
                if i in self.dirty:
                    
                    self.dirty.remove(i)
                    bar_height = height * (self.values[i] / self.maximum)

                    pygame.draw.rect(surface, (0, 0, 0), (bar_x, y, bar_width, height))
                    pygame.draw.rect(surface, self.get_color(i), (bar_x, y + (height - bar_height), bar_width, bar_height))
                bar_x += bar_width

    def draw_all(self, surface, x, y, width, height):
        self.dirty = set()
        bar_width = max(int(width / len(self.values)), 1)
        bar_x = 0
        pygame.draw.rect(surface, (0, 0, 0), (x, y, width, height))
        for i in range(len(self.values)):
            bar_height = height * (self.values[i] / self.maximum)
            
            pygame.draw.rect(surface, self.get_color(i), (bar_x, y + (height - bar_height), bar_width, bar_height))
            
            bar_x += bar_width
