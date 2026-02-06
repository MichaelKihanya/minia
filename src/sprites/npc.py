import pygame
import random
from src.utils.constants import *

def create_npc_sprite(npc_type='villager'):
    """Create sprite for NPC"""
    sprite = pygame.Surface((32, 32), pygame.SRCALPHA)
    
    if npc_type == 'yoga_master':
        # Purple yoga instructor
        pygame.draw.circle(sprite, SKIN_COLOR, (16, 10), 6)
        pygame.draw.rect(sprite, (180, 100, 180), (8, 16, 16, 16))
        pygame.draw.rect(sprite, SKIN_COLOR, (4, 16, 4, 8))
        pygame.draw.rect(sprite, SKIN_COLOR, (24, 16, 4, 8))
        pygame.draw.rect(sprite, SKIN_COLOR, (10, 24, 4, 8))
        pygame.draw.rect(sprite, SKIN_COLOR, (18, 24, 4, 8))
    
    elif npc_type == 'surfer':
        # Orange/tan surfer
        pygame.draw.circle(sprite, SKIN_COLOR, (16, 10), 6)
        pygame.draw.rect(sprite, (255, 165, 0), (8, 16, 16, 16))
        pygame.draw.rect(sprite, SKIN_COLOR, (4, 16, 4, 8))
        pygame.draw.rect(sprite, SKIN_COLOR, (24, 16, 4, 8))
        pygame.draw.circle(sprite, BLACK, (13, 8), 1)
        pygame.draw.circle(sprite, BLACK, (19, 8), 1)
    
    elif npc_type == 'merchant':
        # Brown merchant with hat
        pygame.draw.circle(sprite, SKIN_COLOR, (16, 10), 6)
        pygame.draw.rect(sprite, (139, 69, 19), (8, 16, 16, 16))
        pygame.draw.rect(sprite, (100, 50, 0), (6, 4, 20, 6))  # Hat
        pygame.draw.rect(sprite, SKIN_COLOR, (4, 16, 4, 8))
        pygame.draw.rect(sprite, SKIN_COLOR, (24, 16, 4, 8))
    
    return sprite

class NPC(pygame.sprite.Sprite):
    """Non-player character with dialogue and movement"""
    def __init__(self, x, y, npc_type='villager', name='', dialogue_list=None):
        super().__init__()
        self.grid_x = x
        self.grid_y = y
        self.npc_type = npc_type
        self.name = name
        self.dialogue = dialogue_list or []
        self.current_dialogue = 0
        
        self.image = create_npc_sprite(npc_type)
        self.rect = self.image.get_rect()
        self.rect.x = x * 32
        self.rect.y = y * 32
        
        # Movement
        self.move_timer = 0
        self.move_direction = None
        self.idle_time = random.randint(20, 60)
        self.is_moving = False
        self.move_progress = 0
    
    def update(self, delta_time=0.016):
        """Update NPC movement and behavior"""
        self.move_timer += delta_time
        
        if self.is_moving:
            self.move_progress += 0.1
            if self.move_progress >= 1:
                self.move_progress = 0
                self.is_moving = False
                self.move_timer = 0
                self.idle_time = random.randint(20, 60)
        else:
            # Idle behavior - occasionally move
            if self.move_timer > self.idle_time and random.random() > 0.7:
                directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (0, 0)]
                dx, dy = random.choice(directions)
                
                new_x = self.grid_x + dx
                new_y = self.grid_y + dy
                
                if 0 <= new_x < 20 and 0 <= new_y < 30:
                    self.grid_x = new_x
                    self.grid_y = new_y
                    self.is_moving = True
                    self.move_timer = 0
        
        # Update position
        self.rect.x = self.grid_x * 32
        self.rect.y = self.grid_y * 32
    
    def get_dialogue(self):
        """Get current dialogue"""
        if self.dialogue:
            text = self.dialogue[self.current_dialogue % len(self.dialogue)]
            return f"{self.name}: {text}"
        return ""
    
    def next_dialogue(self):
        """Cycle to next dialogue"""
        self.current_dialogue += 1
