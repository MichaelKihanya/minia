import pygame
import sys
import random
from src.utils.constants import *
from src.sprites.player import Player
from src.sprites.musical_note import MusicalNote
from src.sprites.yoga_pose import YogaPose
from src.world.level import Level

# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Set up the display
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Minia")
clock = pygame.time.Clock()

# Font
font = pygame.font.Font(None, 36)

class Game:
    def __init__(self):
        self.level = Level()
        self.player = Player(100, WINDOW_HEIGHT - 150)  # Start position
        self.all_sprites = pygame.sprite.Group()
        self.notes = pygame.sprite.Group()
        self.yoga_poses = pygame.sprite.Group()
        self.all_sprites.add(self.player)
        
        # Add some musical notes
        for _ in range(5):
            note = MusicalNote(
                random.randint(0, WORLD_WIDTH - 20),
                random.randint(0, WINDOW_HEIGHT - 100)
            )
            self.notes.add(note)
            self.all_sprites.add(note)
            
        # Add yoga poses
        for _ in range(3):
            pose = YogaPose(
                random.randint(0, WORLD_WIDTH - 40),
                random.randint(0, WINDOW_HEIGHT - 100)
            )
            self.yoga_poses.add(pose)
            self.all_sprites.add(pose)
            
        self.score = 0
        self.dialogue = [
            "¡Hola! ¿Te gusta la música?",
            "¡Vamos a cantar juntos!",
            "¿Quieres hacer yoga?",
            "¡Eres muy especial! 💖",
            "¡Excelente pose!",
            "¡Muy bien! ¡Has encontrado una nota musical!"
        ]
        self.current_dialogue = 0
        self.show_dialogue = False
        self.dialogue_timer = 0

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    self.show_dialogue = not self.show_dialogue
                if event.key == pygame.K_m:
                    # Toggle music (to be implemented)
                    pass
                if event.key == pygame.K_y and not self.player.doing_yoga:
                    # Find nearest yoga pose
                    nearest_pose = None
                    min_dist = float('inf')
                    for pose in self.yoga_poses:
                        dist = ((pose.rect.centerx - self.player.rect.centerx) ** 2 +
                               (pose.rect.centery - self.player.rect.centery) ** 2) ** 0.5
                        if dist < min_dist:
                            min_dist = dist
                            nearest_pose = pose
                    
                    if nearest_pose and min_dist < 50:  # If within 50 pixels
                        self.player.start_yoga_pose(nearest_pose.pose_type)
                        self.current_dialogue = 4
                        self.show_dialogue = True
                        self.dialogue_timer = DIALOGUE_DURATION
        return True

    def update(self):
        # Update level (camera)
        self.level.update(self.player)
        
        # Update player with platform collisions
        self.player.update(self.level.platforms)
        
        # Update all other sprites
        self.notes.update()
        self.yoga_poses.update()
        
        # Check for note collection
        note_hits = pygame.sprite.spritecollide(self.player, self.notes, True)
        for note in note_hits:
            self.score += 10
            self.current_dialogue = 5
            self.show_dialogue = True
            self.dialogue_timer = DIALOGUE_DURATION
            # Create new note
            new_note = MusicalNote(
                random.randint(0, WORLD_WIDTH - 20),
                random.randint(0, WINDOW_HEIGHT - 100)
            )
            self.notes.add(new_note)
            self.all_sprites.add(new_note)
            
        # Update dialogue timer
        if self.dialogue_timer > 0:
            self.dialogue_timer -= 1/FPS
            if self.dialogue_timer <= 0:
                self.show_dialogue = False

    def draw(self):
        # Draw level (background and platforms)
        self.level.draw(screen)
        
        # Draw all sprites with camera offset
        for sprite in self.all_sprites:
            screen.blit(sprite.image, 
                       (sprite.rect.x - self.level.camera_x, sprite.rect.y))
        
        # Draw score
        score_text = font.render(f"Puntos: {self.score}", True, BLACK)
        screen.blit(score_text, (10, 10))
        
        # Draw dialogue if active
        if self.show_dialogue:
            dialogue_text = font.render(self.dialogue[self.current_dialogue], True, BLACK)
            text_rect = dialogue_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 100))
            screen.blit(dialogue_text, text_rect)
            
        # Draw yoga timer if doing yoga
        if self.player.doing_yoga:
            yoga_text = font.render(f"¡Mantén la pose! {YOGA_HOLD_TIME - int(self.player.yoga_timer)}", True, BLACK)
            text_rect = yoga_text.get_rect(center=(WINDOW_WIDTH // 2, 50))
            screen.blit(yoga_text, text_rect)
        
        pygame.display.flip()

    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            clock.tick(FPS)

if __name__ == "__main__":
    game = Game()
    game.run()
    pygame.quit()
    sys.exit() 