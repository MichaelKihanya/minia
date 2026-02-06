import pygame
import random
from src.utils.constants import *

def create_pose_indicator(pose_type):
    sprite = pygame.Surface((32, 32), pygame.SRCALPHA)
    
    # Draw a square background with rounded corners effect
    pygame.draw.rect(sprite, PINK, (4, 4, 24, 24))
    
    # Draw pose-specific symbol centered
    if pose_type == 'tree':
        # Draw a tree symbol - more square/geometric
        pygame.draw.rect(sprite, WHITE, (14, 8, 4, 16))  # trunk
        pygame.draw.rect(sprite, WHITE, (8, 12, 16, 4))   # top of tree (cross)
    elif pose_type == 'warrior':
        # Draw a warrior symbol - more square/geometric
        pygame.draw.rect(sprite, WHITE, (10, 14, 12, 2))  # arms
        pygame.draw.rect(sprite, WHITE, (14, 8, 4, 16))   # body/spine
        pygame.draw.rect(sprite, WHITE, (10, 22, 4, 4))   # left leg
        pygame.draw.rect(sprite, WHITE, (18, 22, 4, 4))   # right leg
    else:  # mountain pose
        # Draw a mountain symbol - triangle made from squares
        pygame.draw.polygon(sprite, WHITE, [(8, 24), (16, 8), (24, 24)])
    
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