import pygame
from .paddle import Paddle
from .ball import Ball

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

class GameEngine:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.paddle_width = 10
        self.paddle_height = 100
        self.player = Paddle(10, height // 2 - 50, self.paddle_width, self.paddle_height)
        self.ai = Paddle(width - 20, height // 2 - 50, self.paddle_width, self.paddle_height)
        self.ball = Ball(width // 2, height // 2, 7, 7, width, height)
        self.player_score = 0
        self.ai_score = 0
        self.target_score = 5
        self.font = pygame.font.SysFont("Arial", 30)
        self.large_font = pygame.font.SysFont("Arial", 60)
        self.game_over = False
        self.winner = None

    def handle_input(self):
        """Handle player movement (W/S)."""
        keys = pygame.key.get_pressed()
        if not self.game_over: 
            if keys[pygame.K_w]:
                self.player.move(-10, self.height)
            if keys[pygame.K_s]:
                self.player.move(10, self.height)

    def update(self):
        """Main update loop for gameplay."""
        if self.game_over:
            return  
        self.ball.move()
        self.ball.check_collision(self.player, self.ai)
        if self.ball.x <= 0:
            self.ai_score += 1
            self.ball.reset()
        elif self.ball.x >= self.width:
            self.player_score += 1
            self.ball.reset()
        self.ai.auto_track(self.ball, self.height)
        self.check_game_over()

    def check_game_over(self):
        """Check if either player has reached target score."""
        if self.player_score >= self.target_score:
            self.winner = "Player"
            self.game_over = True
        elif self.ai_score >= self.target_score:
            self.winner = "AI"
            self.game_over = True

    def render(self, screen):
        """Draw all objects and text."""
        screen.fill(BLACK)
        pygame.draw.rect(screen, WHITE, self.player.rect())
        pygame.draw.rect(screen, WHITE, self.ai.rect())
        pygame.draw.ellipse(screen, WHITE, self.ball.rect())
        pygame.draw.aaline(screen, WHITE, (self.width // 2, 0), (self.width // 2, self.height))
        player_text = self.font.render(str(self.player_score), True, WHITE)
        ai_text = self.font.render(str(self.ai_score), True, WHITE)
        screen.blit(player_text, (self.width // 4, 20))
        screen.blit(ai_text, (self.width * 3 // 4, 20))
        if self.game_over:
            self.show_game_over(screen)

    def show_game_over(self, screen):
        """Display winner and replay options."""
        winner_text = self.large_font.render(f"{self.winner} Wins!", True, WHITE)
        screen.blit(winner_text, (self.width // 2 - 150, self.height // 2 - 100))
        font_small = pygame.font.SysFont("Arial", 28)
        options = [
            "Press 3 for Best of 3",
            "Press 5 for Best of 5",
            "Press 7 for Best of 7",
            "Press ESC to Exit"
        ]
        for i, opt in enumerate(options):
            line = font_small.render(opt, True, WHITE)
            screen.blit(line, (self.width // 2 - 150, self.height // 2 + i * 40))

        pygame.display.flip()
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        return
                    elif event.key in [pygame.K_3, pygame.K_5, pygame.K_7]:
                        self.target_score = int(event.unicode)
                        self.reset_game()
                        waiting = False

    def reset_game(self):
        """Reset scores and ball for new match."""
        self.player_score = 0
        self.ai_score = 0
        self.ball.reset()
        self.game_over = False
        self.winner = None