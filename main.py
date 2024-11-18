import pygame
import random

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 600
CAT_WIDTH = 100
CAT_HEIGHT = 50
GRAVITY = 0.5
FLAP_STRENGTH = -10
PIPE_WIDTH = 20
PIPE_GAP = 350
FPS = 60
SPEED_INCREMENT = 1.05  # Factor to increase speed of pipes as the score increases
PIPE_FREQUENCY_DECREASE = 0.95  # Factor to decrease time between pipe spawns
COIN_WIDTH = 30
COIN_HEIGHT = 30
GEM_WIDTH = 40
GEM_HEIGHT = 40

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (10, 55, 30)
LIGHTBLUE = (173, 216, 230)
GOLD = (255, 215, 4)
PURPLE = (128, 0, 128)  # Gem color

# Load images
cat_image = pygame.image.load('IMG_00.JPG')
cat_image = pygame.transform.scale(cat_image, (CAT_WIDTH, CAT_HEIGHT))
coin_image = pygame.Surface((COIN_WIDTH, COIN_HEIGHT))
pygame.draw.circle(coin_image, GOLD, (COIN_WIDTH // 2, COIN_HEIGHT // 2), COIN_WIDTH // 2)
gem_image = pygame.Surface((GEM_WIDTH, GEM_HEIGHT))
pygame.draw.polygon(gem_image, PURPLE, [(GEM_WIDTH // 2, 0), (GEM_WIDTH, GEM_HEIGHT), (GEM_WIDTH // 2, GEM_HEIGHT - 10), (0, GEM_HEIGHT)])

class Cat:
    def __init__(self):
        self.x = 50
        self.y = SCREEN_HEIGHT // 2
        self.velocity = 0
        self.combo_counter = 0  # Track the combo streak
        self.combo_multiplier = 1  # Initial combo multiplier

    def flap(self):
        self.velocity = FLAP_STRENGTH

    def update(self):
        self.velocity += GRAVITY
        self.y += self.velocity
        # Prevent cat from going off-screen
        if self.y < 0:
            self.y = 0
            self.velocity = 0
        elif self.y > SCREEN_HEIGHT - CAT_HEIGHT:
            self.y = SCREEN_HEIGHT - CAT_HEIGHT
            self.velocity = 0

    def reset_combo(self):
        self.combo_counter = 0
        self.combo_multiplier = 1

    def increment_combo(self):
        self.combo_counter += 1
        if self.combo_counter >= 5:
            self.combo_multiplier = 2  # Double score multiplier for combo of 5 or more
        if self.combo_counter >= 10:
            self.combo_multiplier = 3  # Triple score multiplier for combo of 10 or more

class Pipe:
    def __init__(self):
        self.x = SCREEN_WIDTH
        self.height = random.randint(100, 400)
        self.passed = False
        self.speed = 5  # Starting speed of the pipes

    def update(self):
        self.x -= self.speed

    def draw(self, screen):
        # Draw upper pipe
        pygame.draw.rect(screen, GREEN, (self.x, 0, PIPE_WIDTH, self.height))
        # Draw lower pipe
        pygame.draw.rect(screen, GREEN, (self.x, self.height + PIPE_GAP, PIPE_WIDTH, SCREEN_HEIGHT))

class Coin:
    def __init__(self):
        self.x = SCREEN_WIDTH
        self.y = random.randint(100, SCREEN_HEIGHT - 100)
        self.speed = 5  # Same as pipe speed

    def update(self):
        self.x -= self.speed

    def draw(self, screen):
        screen.blit(coin_image, (self.x, self.y))

class Gem:
    def __init__(self):
        self.x = SCREEN_WIDTH
        self.y = random.randint(100, SCREEN_HEIGHT - 100)
        self.speed = 5  # Same as pipe speed

    def update(self):
        self.x -= self.speed

    def draw(self, screen):
        screen.blit(gem_image, (self.x, self.y))

def show_title_screen(screen):
    font = pygame.font.SysFont(None, 64)
    title_text = font.render("Flappy Cat", True, BLACK)
    instructions_text = pygame.font.SysFont(None, 36).render("Press SPACE to Start", True, BLACK)

    screen.fill(LIGHTBLUE)
    screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, SCREEN_HEIGHT // 4))
    screen.blit(instructions_text, (SCREEN_WIDTH // 2 - instructions_text.get_width() // 2, SCREEN_HEIGHT // 2))

    pygame.display.flip()

    # Wait for space key to start the game
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                waiting = False

def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    # Show the title screen
    show_title_screen(screen)

    cat = Cat()
    pipes = []
    coins = []
    gems = []
    score = 0
    frame_count = 0
    pipe_frequency = 40  # Frequency of pipe spawn (frames)
    pipe_gap = PIPE_GAP  # The gap between the pipes
    running = True

    while running:
        screen.fill(LIGHTBLUE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    cat.flap()

        # Update cat
        cat.update()
        screen.blit(cat_image, (cat.x, cat.y))

        # Spawn pipes, coins, and gems at decreasing intervals
        if frame_count % pipe_frequency == 0:
            pipes.append(Pipe())
            if random.random() < 0.5:  # 50% chance to spawn a coin
                coins.append(Coin())
            if random.random() < 0.3:  # 30% chance to spawn a gem
                gems.append(Gem())

        # Update and draw pipes
        for pipe in pipes:
            pipe.update()
            pipe.draw(screen)
            # Check if the cat has passed the pipe
            if pipe.x + PIPE_WIDTH < cat.x and not pipe.passed:
                score += 1 * cat.combo_multiplier  # Apply combo multiplier to score
                pipe.passed = True

        # Update and draw coins
        for coin in coins:
            coin.update()
            coin.draw(screen)
            # Check if the cat has collected the coin
            if (coin.x < cat.x + CAT_WIDTH and coin.x + COIN_WIDTH > cat.x and
                    coin.y < cat.y + CAT_HEIGHT and coin.y + COIN_HEIGHT > cat.y):
                score += 1
                cat.increment_combo()  # Increase combo for coins
                coins.remove(coin)

        # Update and draw gems
        for gem in gems:
            gem.update()
            gem.draw(screen)
            # Check if the cat has collected the gem
            if (gem.x < cat.x + CAT_WIDTH and gem.x + GEM_WIDTH > cat.x and
                    gem.y < cat.y + CAT_HEIGHT and gem.y + GEM_HEIGHT > cat.y):
                score += 5  # Gems are worth more
                cat.increment_combo()  # Increase combo for gems
                gems.remove(gem)

        # Remove off-screen pipes, coins, and gems
        pipes = [pipe for pipe in pipes if pipe.x > -PIPE_WIDTH]
        coins = [coin for coin in coins if coin.x > -COIN_WIDTH]
        gems = [gem for gem in gems if gem.x > -GEM_WIDTH]

        # Draw score
        font = pygame.font.SysFont(None, 36)
        score_text = font.render(f'Score: {score}', True, BLACK)
        screen.blit(score_text, (10, 10))

        # Draw combo multiplier
        if cat.combo_multiplier > 1:
            combo_text = pygame.font.SysFont(None, 36).render(f'Combo x{cat.combo_multiplier}', True, BLACK)
            screen.blit(combo_text, (SCREEN_WIDTH - combo_text.get_width() - 10, 10))

        # Check for collisions with pipes
        for pipe in pipes:
            if (cat.x + CAT_WIDTH > pipe.x and cat.x < pipe.x + PIPE_WIDTH and
                    (cat.y < pipe.height or cat.y + CAT_HEIGHT > pipe.height + pipe_gap)):
                running = False  # End game on collision

        pygame.display.flip()
        frame_count += 1
        clock.tick(FPS)

    # Game Over message and option to restart
    font = pygame.font.SysFont(None, 64)
    game_over_text = font.render("Game Over", True, BLACK)
    restart_text = pygame.font.SysFont(None, 36).render("Press SPACE to Restart", True, BLACK)

    screen.fill(LIGHTBLUE)
    screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 3))
    screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, SCREEN_HEIGHT // 2))

    pygame.display.flip()

    # Wait for the player to press SPACE to restart
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                waiting = False
                main()  # Restart the game

if __name__ == '__main__':
    main()
