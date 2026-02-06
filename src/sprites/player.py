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
        self.rect.x = x
        self.rect.y = y
        self.speed = PLAYER_SPEED
        self.jumping = False
        self.velocity_y = 0
        self.gravity = GRAVITY
        self.doing_yoga = False
        self.yoga_timer = 0
        self.facing_right = True
        self.current_pose = None
        self.on_ground = False

    def update(self, platforms):
        keys = pygame.key.get_pressed()
        
        if not self.doing_yoga:
            # Horizontal movement
            if keys[pygame.K_LEFT]:
                self.rect.x -= self.speed
                self.facing_right = False
            if keys[pygame.K_RIGHT]:
                self.rect.x += self.speed
                self.facing_right = True
                
            # Flip sprite based on direction
            self.image = pygame.transform.flip(self.original_image, not self.facing_right, False)
                
            # Jumping
            if keys[pygame.K_SPACE] and self.on_ground:
                self.velocity_y = JUMP_FORCE
                self.jumping = True
                self.on_ground = False
                
            # Apply gravity
            self.velocity_y += self.gravity
            self.rect.y += self.velocity_y
            
            # Platform collisions
            self.on_ground = False
            for platform in platforms:
                if self.rect.colliderect(platform.rect):
                    # Bottom collision
                    if self.velocity_y > 0 and self.rect.bottom > platform.rect.top:
                        self.rect.bottom = platform.rect.top
                        self.velocity_y = 0
                        self.jumping = False
                        self.on_ground = True
                    # Top collision
                    elif self.velocity_y < 0 and self.rect.top < platform.rect.bottom:
                        self.rect.top = platform.rect.bottom
                        self.velocity_y = 0
        else:
            self.yoga_timer += 1/FPS
            if self.yoga_timer >= YOGA_HOLD_TIME:
                self.doing_yoga = False
                self.yoga_timer = 0
                self.image = pygame.transform.flip(self.original_image, not self.facing_right, False)
            
        # Keep player in world bounds
        self.rect.clamp_ip(pygame.Rect(0, 0, WORLD_WIDTH, WINDOW_HEIGHT))

    def start_yoga_pose(self, pose_type):
        self.doing_yoga = True
        self.yoga_timer = 0
        self.current_pose = pose_type
        
        # Set the appropriate yoga pose sprite
        if pose_type == 'tree':
            self.image = pygame.transform.flip(self.tree_pose, not self.facing_right, False)
        elif pose_type == 'warrior':
            self.image = pygame.transform.flip(self.warrior_pose, not self.facing_right, False) 