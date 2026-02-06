import pygame
import sys
import random
import math
from src.utils.constants import *
from src.sprites.player import Player
from src.sprites.musical_note import MusicalNote
from src.sprites.yoga_pose import YogaPose
from src.sprites.npc import NPC
from src.sprites.animation import ParticleEffect, WeatherEffect
from src.world.level import Level

# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Set up the display
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Minia")
clock = pygame.time.Clock()

# Fonts
font = pygame.font.Font(None, 36)
large_font = pygame.font.Font(None, 72)
subtitle_font = pygame.font.Font(None, 28)

class Game:
    def __init__(self):
        self.show_title_screen = True
        self.title_timer = 0
        
        self.level = Level()
        self.player = Player(5, 5)  # Start in town (grid coordinates)
        self.all_sprites = pygame.sprite.Group()
        self.notes = pygame.sprite.Group()
        self.yoga_poses = pygame.sprite.Group()
        self.npcs = pygame.sprite.Group()
        self.all_sprites.add(self.player)
        
        # Add NPCs in different zones
        yoga_master = NPC(
            4, 13, npc_type='yoga_master', name='Maestro Yoga',
            dialogue_list=[
                "The body is a temple, cuida bien 💆",
                "Every breath is a prayer",
                "Tu cuerpo habla verdades",
                "Yoga connects the soul to the earth"
            ]
        )
        self.npcs.add(yoga_master)
        self.all_sprites.add(yoga_master)
        
        surfer = NPC(
            16, 5, npc_type='surfer', name='Marina',
            dialogue_list=[
                "Catch the next wave with your heart!",
                "The ocean teaches us about life's flow",
                "Surfing = freedom + salt water",
                "La vida es como el océano, ¡vívela!"
            ]
        )
        self.npcs.add(surfer)
        self.all_sprites.add(surfer)
        
        merchant = NPC(
            12, 14, npc_type='merchant', name='Taquero',
            dialogue_list=[
                "¡Los mejores tacos de todo el mundo!",
                "Hecho con amor y tradición",
                "Each taco tells a story",
                "Come, sonríe, vive"
            ]
        )
        self.npcs.add(merchant)
        self.all_sprites.add(merchant)
        
        # Particle effects system
        self.particle_effects = []
        self.weather = WeatherEffect('none')
            
        # Add tacos scattered across world (grid coordinates)
        taco_positions = [
            (8, 8),    # Town
            (15, 2),   # Beach
            (12, 15),  # Taco Market
            (3, 18),   # Nature
            (2, 8),    # Town edge
        ]
        for x, y in taco_positions:
            note = MusicalNote(x * 32, y * 32)
            self.notes.add(note)
            self.all_sprites.add(note)
            
        # Add yoga poses in yoga garden (grid coordinates)
        yoga_positions = [
            (3, 13),   # Tree pose
            (5, 13),   # Warrior pose
            (7, 13),   # Mountain pose
        ]
        for i, (x, y) in enumerate(yoga_positions):
            pose_type = ['tree', 'warrior', 'mountain'][i]
            pose = YogaPose(x * 32, y * 32)
            pose.pose_type = pose_type
            self.yoga_poses.add(pose)
            self.all_sprites.add(pose)
            
        self.score = 0
        self.dialogue = [
            "Tania... te amo más cada día 💙",
            "Eres tan hermosa cuando sonríes",
            "Even though we're far apart, you're always in my heart",
            "Te extraño mucho, mi amor",
            "Your yoga journey inspires me every day",
            "¡Encontraste un taco! Just like I found you 🌮💕",
            "Thinking of you always",
            "Eres mi todo, Tania",
            "Your inner peace is so beautiful to see",
            "You flow like water through every pose, hermosa",
            "Namaste, mi amor 🧘‍♀️💕",
            "Your strength and grace take my breath away"
        ]
        self.current_dialogue = 0
        self.show_dialogue = False
        self.dialogue_timer = 0

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if self.show_title_screen:
                    self.show_title_screen = False
                elif event.key == pygame.K_e:
                    self.show_dialogue = not self.show_dialogue
                if event.key == pygame.K_m:
                    # Toggle music (to be implemented)
                    pass
                if event.key == pygame.K_y and not self.player.doing_yoga:
                    # Check if player is on a yoga pose tile
                    for pose in self.yoga_poses:
                        if self.player.grid_x * 32 == pose.rect.x and self.player.grid_y * 32 == pose.rect.y:
                            self.player.start_yoga_pose(pose.pose_type)
                            # Yoga-specific dialogue based on pose type
                            if pose.pose_type == 'tree':
                                self.current_dialogue = 9  # "You flow like water..."
                            elif pose.pose_type == 'warrior':
                                self.current_dialogue = 11  # "Your strength and grace..."
                            else:  # mountain
                                self.current_dialogue = 10  # "Namaste..."
                            self.show_dialogue = True
                            self.dialogue_timer = DIALOGUE_DURATION * 1.5
                            break
        return True

    def update(self):
        if self.show_title_screen:
            self.title_timer += 1/FPS
            return
            
        # Update level (camera)
        self.level.update(self.player)
        
        # Update player with platform collisions
        self.player.update(self.level.platforms)
        
        # Update all other sprites
        self.notes.update()
        self.yoga_poses.update()
        self.npcs.update()
        
        # Update weather
        self.weather.update()
        
        # Update particle effects
        dead_effects = []
        for effect in self.particle_effects:
            if effect.update(1/FPS):
                dead_effects.append(effect)
        for effect in dead_effects:
            self.particle_effects.remove(effect)
        
        # Check for taco collection (grid-based)
        for taco in self.notes:
            if self.player.grid_x * 32 == taco.rect.x and self.player.grid_y * 32 == taco.rect.y:
                self.score += 1
                self.current_dialogue = 5
                self.show_dialogue = True
                self.dialogue_timer = DIALOGUE_DURATION
                
                # Add particle effect
                if ENABLE_PARTICLES:
                    self.particle_effects.append(
                        ParticleEffect(self.player.rect.x, self.player.rect.y, 'sparkle', 0.5)
                    )
                
                # Remove the collected taco and respawn elsewhere
                self.notes.remove(taco)
                self.all_sprites.remove(taco)
                
                # Respawn taco in random location
                import random as rnd
                new_x = rnd.randint(2, 18)
                new_y = rnd.randint(2, 28)
                new_taco = MusicalNote(new_x * 32, new_y * 32)
                self.notes.add(new_taco)
                self.all_sprites.add(new_taco)
            
        # Update dialogue timer
        if self.dialogue_timer > 0:
            self.dialogue_timer -= 1/FPS
            if self.dialogue_timer <= 0:
                self.show_dialogue = False

    def draw(self):
        if self.show_title_screen:
            # Draw title screen
            screen.fill((200, 190, 180))  # Soft beige background
            
            # Main title
            title_text = large_font.render("For Tania", True, (100, 60, 40))
            title_rect = title_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 3))
            screen.blit(title_text, title_rect)
            
            # Subtitle
            subtitle = subtitle_font.render("A love letter in a game", True, (130, 100, 90))
            subtitle_rect = subtitle.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 3 + 80))
            screen.blit(subtitle, subtitle_rect)
            
            # Message
            message = font.render("Mi amor, I made this for you 💙", True, (100, 80, 100))
            message_rect = message.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 40))
            screen.blit(message, message_rect)
            
            # Press any key
            prompt = subtitle_font.render("Press any key to start...", True, (120, 90, 80))
            prompt_rect = prompt.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT - 100))
            
            # Fade effect
            alpha = int(255 * (0.5 + 0.5 * math.sin(self.title_timer * 3)))
            prompt.set_alpha(alpha)
            screen.blit(prompt, prompt_rect)
            
            pygame.display.flip()
            return
        
        # Draw level (background and grid)
        self.level.draw(screen)
        
        # Draw tacos and yoga poses (but not player or NPCs)
        for sprite in self.all_sprites:
            if sprite != self.player and not isinstance(sprite, NPC):
                screen_x = sprite.rect.x - self.level.camera_x
                screen_y = sprite.rect.y - self.level.camera_y
                screen.blit(sprite.image, (screen_x, screen_y))
        
        # Draw NPCs
        for npc in self.npcs:
            screen_x = npc.rect.x - self.level.camera_x
            screen_y = npc.rect.y - self.level.camera_y
            screen.blit(npc.image, (screen_x, screen_y))
            
            # Draw NPC name label
            name_font = pygame.font.Font(None, 16)
            name_text = name_font.render(npc.name, True, BLACK)
            name_rect = name_text.get_rect(center=(screen_x + 16, screen_y - 10))
            screen.blit(name_text, name_rect)
        
        # Draw player on top (always visible)
        screen_x = self.player.rect.x - self.level.camera_x
        screen_y = self.player.rect.y - self.level.camera_y
        screen.blit(self.player.image, (screen_x, screen_y))
        
        # Draw particle effects
        for effect in self.particle_effects:
            effect.draw(screen, self.level.camera_x, self.level.camera_y)
        
        # Draw weather
        self.weather.draw(screen)
        
        # Draw score
        score_text = font.render(f"Tacos encontrados: {self.score}", True, BLACK)
        screen.blit(score_text, (10, 10))
        
        # Draw controls hint
        hint_text = font.render("Arrow Keys: Move | Y: Yoga | E: Talk", True, (120, 100, 90))
        screen.blit(hint_text, (10, WINDOW_HEIGHT - 35))
        
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