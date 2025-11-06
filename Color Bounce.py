import pygame
import random

pygame.init()

# --- Constants
WIDTH, HEIGHT = 500, 500

SPRITE_COLOR_CHANGE_EVENT = pygame.USEREVENT + 1
BACKGROUND_COLOR_CHANGE_EVENT = pygame.USEREVENT + 2

BLUE = pygame.Color('blue')
LIGHTBLUE = pygame.Color('lightblue')
DARKBLUE = pygame.Color('darkblue')

YELLOW = pygame.Color('yellow')
MAGENTA = pygame.Color('magenta')
ORANGE = pygame.Color('orange')
WHITE = pygame.Color('white')

# --- Sprite
class Sprite(pygame.sprite.Sprite):
    def __init__(self, color, height, width):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        # velocity will be either -1 or 1 on each axis
        self.velocity = [random.choice([-1, 1]), random.choice([-1, 1])]

    def update(self):
        self.rect.move_ip(self.velocity)
        boundary_hit = False

        # Bounce on window edges
        if self.rect.left <= 0 or self.rect.right >= WIDTH:
            self.velocity[0] = -self.velocity[0]
            boundary_hit = True
        if self.rect.top <= 0 or self.rect.bottom >= HEIGHT:
            self.velocity[1] = -self.velocity[1]
            boundary_hit = True

        # Post events when we hit a boundary
        if boundary_hit:
            pygame.event.post(pygame.event.Event(SPRITE_COLOR_CHANGE_EVENT))
            pygame.event.post(pygame.event.Event(BACKGROUND_COLOR_CHANGE_EVENT))

    def change_color(self):
        self.image.fill(random.choice([YELLOW, MAGENTA, ORANGE, WHITE]))


# --- Helpers
def change_background_color():
    return random.choice([BLUE, LIGHTBLUE, DARKBLUE])


def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Boundary Sprite")

    # Sprite setup
    all_sprites = pygame.sprite.Group()
    sp1 = Sprite(WHITE, height=20, width=30)
    # Place the sprite fully on-screen
    sp1.rect.x = random.randint(0, WIDTH - sp1.rect.width)
    sp1.rect.y = random.randint(0, HEIGHT - sp1.rect.height)
    all_sprites.add(sp1)

    bg_color = BLUE
    screen.fill(bg_color)

    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == SPRITE_COLOR_CHANGE_EVENT:
                sp1.change_color()

            elif event.type == BACKGROUND_COLOR_CHANGE_EVENT:
                bg_color = change_background_color()

        all_sprites.update()
        screen.fill(bg_color)
        all_sprites.draw(screen)

        pygame.display.flip()
        clock.tick(240)  # Cap FPS

    pygame.quit()


if __name__ == "__main__":
    main()
