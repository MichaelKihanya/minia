import pygame
import random
from src.utils.constants import *

def create_pose_indicator(pose_type):
    sprite = pygame.Surface((40, 40), pygame.SRCALPHA)
    
    # Draw a circle background
    pygame.draw.circle(sprite, PINK, (20, 20), 15)
    
    # Draw pose-specific symbol
    if pose_type == 'tree':
        # Draw a tree symbol
        pygame.draw.rect(sprite, WHITE, (18, 10, 4, 20))  # trunk
        pygame.draw.circle(sprite, WHITE, (20, 8), 8)     # leaves
    elif pose_type == 'warrior':
        # Draw a warrior symbol
        pygame.draw.line(sprite, WHITE, (10, 20), (30, 20), 3)  # arms
        pygame.draw.line(sprite, WHITE, (20, 10), (20, 30), 3)  # body
        pygame.draw.line(sprite, WHITE, (15, 30), (25, 30), 3)  # legs
    else:  # mountain pose
        # Draw a mountain symbol
        pygame.draw.polygon(sprite, WHITE, [(10, 30), (20, 10), (30, 30)])
    
    return sprite

class YogaPose(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.pose_type = random.choice(['tree', 'warrior', 'mountain'])
        self.image = create_pose_indicator(self.pose_type)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.active = False
        self.timer = 0
        self.hold_time = YOGA_HOLD_TIME

    def update(self):
        if self.active:
            self.timer += 1/FPS
            if self.timer >= self.hold_time:
                self.active = False
                self.timer = 0 