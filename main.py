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

# Colors
WHITE = (255, 255, 255)
BLACK = (0,0,0)
GREEN = (10, 55, 30)
LIGHTBLUE = (173,216,230)
GOLD = (255,215,4)

# Load images
cat_image = pygame.image.load('IMG_00.JPG')
cat_image = pygame.transform.scale(cat_image, (CAT_WIDTH, CAT_HEIGHT))
coin_image = pygame.Surface((COIN_WIDTH, COIN_HEIGHT))
pygame.draw.circle(coin_image, GOLD, (COIN_WIDTH // 2, COIN_HEIGHT // 2), COIN_WIDTH // 2)

class Cat:
    def __init__(self):
        self.x = 50
        self.y = SCREEN_HEIGHT // 2
        self.velocity = 0

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

def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    cat = Cat()
    pipes = []
    coins = []
    score = 0
    frame_count = 0
    pipe_frequency = 90  # Frequency of pipe spawn (frames)
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

        # Spawn pipes at decreasing intervals
        if frame_count % pipe_frequency == 0:
            pipes.append(Pipe())
            # Random chance to spawn a coin with each pipe
            if random.random() < 0.5:  # 50% chance to spawn a coin with each pipe
                coins.append(Coin())

        # Update and draw pipes
        for pipe in pipes:
            pipe.update()
            pipe.draw(screen)
            # Check if the cat has passed the pipe
            if pipe.x + PIPE_WIDTH < cat.x and not pipe.passed:
                score += 1
                pipe.passed = True

        # Update and draw coins
        for coin in coins:
            coin.update()
            coin.draw(screen)
            # Check if the cat has collected the coin
            if (coin.x < cat.x + CAT_WIDTH and coin.x + COIN_WIDTH > cat.x and
                    coin.y < cat.y + CAT_HEIGHT and coin.y + COIN_HEIGHT > cat.y):
                score += 1
                coins.remove(coin)

        # Remove off-screen pipes and coins
        pipes = [pipe for pipe in pipes if pipe.x > -PIPE_WIDTH]
        coins = [coin for coin in coins if coin.x > -COIN_WIDTH]

        # Draw score
        font = pygame.font.SysFont(None, 36)
        score_text = font.render(f'Score: {score}', True, (0, 0, 0))
        screen.blit(score_text, (10, 10))

        # Check for collisions with pipes
        for pipe in pipes:
            if (cat.x + CAT_WIDTH > pipe.x and cat.x < pipe.x + PIPE_WIDTH and
                    (cat.y < pipe.height or cat.y + CAT_HEIGHT > pipe.height + pipe_gap)):
                running = False  # End game on collision



        pygame.display.flip()
        frame_count += 1
        clock.tick(FPS)

    pygame.quit()

if __name__ == '__main__':
    main()
