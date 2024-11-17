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

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

# Load cat image (make sure you have a cat image named 'cat.png' in the same directory)
cat_image = pygame.image.load('IMG_00.JPG')
cat_image = pygame.transform.scale(cat_image, (CAT_WIDTH, CAT_HEIGHT))


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


def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    cat = Cat()
    pipes = []
    score = 0
    frame_count = 0
    pipe_frequency = 90  # Frequency of pipe spawn (frames)
    pipe_gap = PIPE_GAP  # The gap between the pipes
    running = True

    while running:
        screen.fill(WHITE)

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

        # Update and draw pipes
        for pipe in pipes:
            pipe.update()
            pipe.draw(screen)
            # Check if the cat has passed the pipe
            if pipe.x + PIPE_WIDTH < cat.x and not pipe.passed:
                score += 1
                pipe.passed = True

        # Remove off-screen pipes
        pipes = [pipe for pipe in pipes if pipe.x > -PIPE_WIDTH]

        # Draw score
        font = pygame.font.SysFont(None, 36)
        score_text = font.render(f'Score: {score}', True, (0, 0, 0))
        screen.blit(score_text, (10, 10))

        # Check for collisions
        for pipe in pipes:
            if (cat.x + CAT_WIDTH > pipe.x and cat.x < pipe.x + PIPE_WIDTH and
                    (cat.y < pipe.height or cat.y + CAT_HEIGHT > pipe.height + pipe_gap)):
                running = False  # End game on collision

        # Increase difficulty over time
        if score > 0 and score % 5 == 0:  # Every 5 points
            # Speed up pipes
            for pipe in pipes:
                pipe.speed *= SPEED_INCREMENT
            # Decrease pipe spawn frequency
            pipe_frequency = max(30, int(pipe_frequency * PIPE_FREQUENCY_DECREASE))
            # Make the pipe gap smaller
            pipe_gap = max(100, pipe_gap - 10)
            # Make gravity stronger
            global GRAVITY
            GRAVITY += 0.1

        pygame.display.flip()
        frame_count += 1
        clock.tick(FPS)

    pygame.quit()


if __name__ == '__main__':
    main()
