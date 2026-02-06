import pygame
import math
from src.utils.constants import *

def create_cute_sprite():
    # Create a 32x32 surface for the sprite
    sprite = pygame.Surface((32, 32), pygame.SRCALPHA)
    
    # Draw body (dress)
    pygame.draw.rect(sprite, DRESS_COLOR, (8, 16, 16, 16))
    
    # Draw head
    pygame.draw.circle(sprite, SKIN_COLOR, (16, 12), 8)
    
    # Draw hair
    pygame.draw.rect(sprite, HAIR_COLOR, (8, 4, 16, 8))
    pygame.draw.rect(sprite, HAIR_COLOR, (4, 8, 24, 4))
    
    # Draw eyes
    pygame.draw.circle(sprite, BLACK, (13, 10), 2)  # Left eye
    pygame.draw.circle(sprite, BLACK, (19, 10), 2)  # Right eye
    
    # Draw smile
    pygame.draw.arc(sprite, BLACK, (12, 10, 8, 6), 0, math.pi)
    
    # Draw arms
    pygame.draw.rect(sprite, SKIN_COLOR, (4, 16, 4, 8))
    pygame.draw.rect(sprite, SKIN_COLOR, (24, 16, 4, 8))
    
    # Draw legs
    pygame.draw.rect(sprite, SKIN_COLOR, (12, 32, 4, 8))
    pygame.draw.rect(sprite, SKIN_COLOR, (16, 32, 4, 8))
    
    return sprite

def create_tree_pose_sprite():
    sprite = pygame.Surface((32, 32), pygame.SRCALPHA)
    
    # Draw body (dress)
    pygame.draw.rect(sprite, DRESS_COLOR, (8, 16, 16, 16))
    
    # Draw head
    pygame.draw.circle(sprite, SKIN_COLOR, (16, 12), 8)
    
    # Draw hair
    pygame.draw.rect(sprite, HAIR_COLOR, (8, 4, 16, 8))
    pygame.draw.rect(sprite, HAIR_COLOR, (4, 8, 24, 4))
    
    # Draw eyes (closed for meditation)
    pygame.draw.line(sprite, BLACK, (13, 10), (19, 10), 2)
    
    # Draw arms (raised)
    pygame.draw.rect(sprite, SKIN_COLOR, (4, 8, 4, 16))
    pygame.draw.rect(sprite, SKIN_COLOR, (24, 8, 4, 16))
    
    # Draw legs (one bent)
    pygame.draw.rect(sprite, SKIN_COLOR, (12, 32, 4, 8))
    pygame.draw.rect(sprite, SKIN_COLOR, (16, 32, 4, 8))
    
    return sprite

def create_warrior_pose_sprite():
    sprite = pygame.Surface((32, 32), pygame.SRCALPHA)
    
    # Draw body (dress)
    pygame.draw.rect(sprite, DRESS_COLOR, (8, 16, 16, 16))
    
    # Draw head
    pygame.draw.circle(sprite, SKIN_COLOR, (16, 12), 8)
    
    # Draw hair
    pygame.draw.rect(sprite, HAIR_COLOR, (8, 4, 16, 8))
    pygame.draw.rect(sprite, HAIR_COLOR, (4, 8, 24, 4))
    
    # Draw eyes (determined)
    pygame.draw.circle(sprite, BLACK, (13, 10), 2)
    pygame.draw.circle(sprite, BLACK, (19, 10), 2)
    
    # Draw arms (extended)
    pygame.draw.rect(sprite, SKIN_COLOR, (0, 16, 4, 8))
    pygame.draw.rect(sprite, SKIN_COLOR, (28, 16, 4, 8))
    
    # Draw legs (wide stance)
    pygame.draw.rect(sprite, SKIN_COLOR, (8, 32, 4, 8))
    pygame.draw.rect(sprite, SKIN_COLOR, (20, 32, 4, 8))
    
    return sprite

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.original_image = create_cute_sprite()
        self.tree_pose = create_tree_pose_sprite()
        self.warrior_pose = create_warrior_pose_sprite()
        self.image = self.original_image
        self.rect = self.image.get_rect()
        
        # Grid-based position (in grid coordinates, will convert to pixels)
        self.grid_x = x
        self.grid_y = y
        self.rect.x = x * 32
        self.rect.y = y * 32
        
        self.facing_right = True
        self.doing_yoga = False
        self.yoga_timer = 0
        self.current_pose = None
        
        # Movement animation
        self.move_progress = 0  # 0 to 1, for smooth movement between tiles
        self.is_moving = False
        self.move_direction = None  # (dx, dy)
        self.move_speed = 0.2  # tiles per frame

    def update(self, platforms=None):
        """Update player with grid-based movement"""
        keys = pygame.key.get_pressed()
        
        if not self.doing_yoga:
            # Handle grid movement
            move_x = 0
            move_y = 0
            
            if keys[pygame.K_LEFT]:
                move_x = -1
                self.facing_right = False
            elif keys[pygame.K_RIGHT]:
                move_x = 1
                self.facing_right = True
            elif keys[pygame.K_UP]:
                move_y = -1
            elif keys[pygame.K_DOWN]:
                move_y = 1
            
            # Move to adjacent tile if not already moving
            if (move_x != 0 or move_y != 0) and not self.is_moving:
                # Check bounds (20x30 tile world)
                new_x = self.grid_x + move_x
                new_y = self.grid_y + move_y
                
                if 0 <= new_x < 20 and 0 <= new_y < 30:
                    self.grid_x = new_x
                    self.grid_y = new_y
                    self.is_moving = True
                    self.move_progress = 0
                    self.move_direction = (move_x, move_y)
            
            # Animate movement between tiles
            if self.is_moving:
                self.move_progress += self.move_speed
                if self.move_progress >= 1:
                    self.move_progress = 1
                    self.is_moving = False
            
            # Update pixel position based on grid and animation progress
            self.rect.x = self.grid_x * 32
            self.rect.y = self.grid_y * 32
            
            # Flip sprite based on direction
            self.image = pygame.transform.flip(self.original_image, not self.facing_right, False)
        else:
            # Yoga animation
            self.yoga_timer += 1/FPS
            if self.yoga_timer >= YOGA_HOLD_TIME:
                self.doing_yoga = False
                self.yoga_timer = 0
                self.image = pygame.transform.flip(self.original_image, not self.facing_right, False)

    def start_yoga_pose(self, pose_type):
        self.doing_yoga = True
        self.yoga_timer = 0
        self.current_pose = pose_type
        
        # Set the appropriate yoga pose sprite
        if pose_type == 'tree':
            self.image = pygame.transform.flip(self.tree_pose, not self.facing_right, False)
        elif pose_type == 'warrior':
            self.image = pygame.transform.flip(self.warrior_pose, not self.facing_right, False) 