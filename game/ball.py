import pygame
import random
import os

class Ball:
    def __init__(self, x, y, width, height, screen_width, screen_height):
        self.original_x = x
        self.original_y = y
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.velocity_x = random.choice([-5, 5])
        self.velocity_y = random.choice([-3, 3])
        self.load_sounds()

    def load_sounds(self):
        """Load sound files."""
        base_path = os.path.dirname(os.path.abspath(__file__))
        self.sound_paddle = pygame.mixer.Sound(os.path.join(base_path, "sounds/paddle_hit.wav"))
        self.sound_wall = pygame.mixer.Sound(os.path.join(base_path, "sounds/wall_bounce.wav"))
        self.sound_score = pygame.mixer.Sound(os.path.join(base_path, "sounds/score.wav"))

    def move(self):
        """Move the ball and handle top/bottom wall collisions."""
        self.x += self.velocity_x
        self.y += self.velocity_y
        if self.y <= 0:
            self.y = 0
            self.velocity_y *= -1
            self.sound_wall.play()
        elif self.y + self.height >= self.screen_height:
            self.y = self.screen_height - self.height
            self.velocity_y *= -1
            self.sound_wall.play()

    def check_collision(self, player, ai):
        """Accurate collision detection for both paddles."""
        ball_rect = self.rect()
        player_rect = player.rect()
        ai_rect = ai.rect()
        if ball_rect.colliderect(player_rect):
            self.x = player_rect.x + player_rect.width
            self.velocity_x = abs(self.velocity_x)
            self.sound_paddle.play()
        elif ball_rect.colliderect(ai_rect):
            self.x = ai_rect.x - self.width
            self.velocity_x = -abs(self.velocity_x)
            self.sound_paddle.play()

    def reset(self):
        """Reset ball to center and randomize direction."""
        self.x = self.original_x
        self.y = self.original_y
        self.velocity_x *= -1
        self.velocity_y = random.choice([-3, 3])
        self.sound_score.play()

    def rect(self):
        """Return pygame.Rect for collision detection."""
        return pygame.Rect(self.x, self.y, self.width, self.height)