import pygame
import math
import random
from src.utils.constants import *

def create_note_sprite():
    sprite = pygame.Surface((20, 20), pygame.SRCALPHA)
    
    # Draw note head
    pygame.draw.circle(sprite, GOLD, (10, 10), 5)
    
    # Draw note stem
    pygame.draw.rect(sprite, GOLD, (12, 2, 2, 16))
    
    # Draw note flag
    pygame.draw.arc(sprite, GOLD, (12, 2, 8, 8), 0, math.pi * 2)
    
    return sprite

class MusicalNote(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = create_note_sprite()
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.float_offset = random.randint(0, 360)
        self.float_speed = 0.05

    def update(self):
        # Make the note float up and down
        self.rect.y += math.sin(pygame.time.get_ticks() * self.float_speed + self.float_offset) * 0.5 