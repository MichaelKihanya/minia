import pygame
import math

class AnimationFrame:
    """Represents a single frame in an animation"""
    def __init__(self, surface, duration=0.1):
        self.surface = surface
        self.duration = duration

class Animation:
    """Manages sprite animations with frame-by-frame control"""
    def __init__(self, frames, loop=True):
        self.frames = frames  # List of AnimationFrame objects
        self.current_frame = 0
        self.elapsed_time = 0
        self.loop = loop
        self.finished = False
    
    def update(self, delta_time):
        """Update animation, returns True if finished"""
        if self.finished and not self.loop:
            return True
        
        self.elapsed_time += delta_time
        frame = self.frames[self.current_frame]
        
        if self.elapsed_time >= frame.duration:
            self.elapsed_time -= frame.duration
            self.current_frame += 1
            
            if self.current_frame >= len(self.frames):
                if self.loop:
                    self.current_frame = 0
                else:
                    self.current_frame = len(self.frames) - 1
                    self.finished = True
        
        return self.finished
    
    def get_current_frame(self):
        """Get current frame surface"""
        if self.current_frame < len(self.frames):
            return self.frames[self.current_frame].surface
        return self.frames[-1].surface

class AnimatedSprite(pygame.sprite.Sprite):
    """Base class for animated sprites"""
    def __init__(self, x, y):
        super().__init__()
        self.rect = pygame.Rect(x, y, 32, 32)
        self.animations = {}
        self.current_animation = None
        self.image = pygame.Surface((32, 32), pygame.SRCALPHA)
    
    def add_animation(self, name, animation):
        """Add animation by name"""
        self.animations[name] = animation
    
    def play_animation(self, name):
        """Play animation by name"""
        if name in self.animations:
            self.current_animation = self.animations[name]
    
    def update(self, delta_time=0.016):
        """Update current animation"""
        if self.current_animation:
            self.current_animation.update(delta_time)
            self.image = self.current_animation.get_current_frame()

class ParticleEffect:
    """Particle effect for visual feedback"""
    def __init__(self, x, y, particle_type='sparkle', duration=0.5):
        self.x = x
        self.y = y
        self.type = particle_type
        self.duration = duration
        self.elapsed = 0
        self.particles = self._create_particles()
    
    def _create_particles(self):
        """Create particles based on type"""
        particles = []
        if self.type == 'sparkle':
            for _ in range(8):
                angle = (360 / 8) * len(particles) * (math.pi / 180)
                particles.append({
                    'x': self.x,
                    'y': self.y,
                    'vx': math.cos(angle) * 2,
                    'vy': math.sin(angle) * 2,
                    'life': self.duration,
                    'color': (255, 215, 0)
                })
        elif self.type == 'yoga_aura':
            for _ in range(12):
                angle = (360 / 12) * len(particles) * (math.pi / 180)
                particles.append({
                    'x': self.x,
                    'y': self.y,
                    'vx': math.cos(angle) * 1,
                    'vy': math.sin(angle) * 1,
                    'life': self.duration,
                    'color': (200, 150, 200)
                })
        return particles
    
    def update(self, delta_time):
        """Update particles"""
        self.elapsed += delta_time
        
        for particle in self.particles:
            particle['x'] += particle['vx']
            particle['y'] += particle['vy']
            particle['life'] -= delta_time
            particle['vy'] += 0.1  # Gravity
        
        return self.elapsed >= self.duration
    
    def draw(self, surface, camera_x, camera_y):
        """Draw particles"""
        for particle in self.particles:
            if particle['life'] > 0:
                alpha = int(255 * (particle['life'] / self.duration))
                size = max(1, int(3 * (particle['life'] / self.duration)))
                
                screen_x = int(particle['x'] - camera_x)
                screen_y = int(particle['y'] - camera_y)
                
                if 0 <= screen_x < 800 and 0 <= screen_y < 600:
                    pygame.draw.circle(surface, particle['color'], (screen_x, screen_y), size)

class WeatherEffect:
    """Weather system for atmospheric effects"""
    def __init__(self, weather_type='none'):
        self.type = weather_type
        self.intensity = 0
        self.particles = []
    
    def set_weather(self, weather_type, intensity=0.5):
        """Set weather type and intensity"""
        self.type = weather_type
        self.intensity = intensity
        self._generate_particles()
    
    def _generate_particles(self):
        """Generate weather particles"""
        import random
        self.particles = []
        if self.type == 'rain':
            count = int(50 * self.intensity)
            for _ in range(count):
                self.particles.append({
                    'x': random.randint(0, 800),
                    'y': random.randint(-100, 600),
                    'vx': random.uniform(-1, 1),
                    'vy': random.uniform(3, 6)
                })
    
    def update(self):
        """Update weather"""
        for particle in self.particles:
            particle['y'] += particle['vy']
            particle['x'] += particle['vx']
            
            # Wrap around
            if particle['y'] > 600:
                particle['y'] = -10
                particle['x'] = (particle['x'] % 800)
    
    def draw(self, surface):
        """Draw weather effects"""
        if self.type == 'rain':
            for particle in self.particles:
                pygame.draw.line(surface, (150, 180, 220), 
                               (particle['x'], particle['y']),
                               (particle['x'] - 2, particle['y'] + 8), 1)
        elif self.type == 'mist':
            surface.fill((200, 200, 200), special_flags=pygame.BLEND_RGBA_MULT)
