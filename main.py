import pygame
import random
import time

pygame.init()

# --- Setup ---
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Alien Freeze Tag")

# Replaced Chicken Sprite
def create_sprite(color, size, shape="rect"):
    surf = pygame.Surface(size, pygame.SRCALPHA)
    if shape == "circle":
        pygame.draw.circle(surf, color, (size[0]//2, size[1]//2), size[0]//2)
    else:
        pygame.draw.rect(surf, color, [0, 0, size[0], size[1]])
    return surf

alien_surf = pygame.image.load("alien.png").convert_alpha() # Green Aliens
star_surf = pygame.image.load("star.png").convert_alpha()   # Golden Powerup

# --- Game Variables ---
num_aliens = 6
aliens = []
for _ in range(num_aliens):
    # Each alien: [x, y, speed]
    aliens.append([
        random.randint(0, WIDTH - 50), 
        random.randint(-400, -50), 
        random.uniform(0.005, 0.1)
    ])

# Powerup variables
powerup_pos = [random.randint(50, WIDTH-50), random.randint(50, HEIGHT-50)]
powerup_active = True
freeze_until = 0

clock = pygame.time.Clock()
running = True

while running:
    current_time = time.time()
    screen.fill((20, 20, 40)) # Dark space background

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos

            # 1. Check Powerup Collision (Clicking the Star)
            star_rect = pygame.Rect(powerup_pos[0], powerup_pos[1], 30, 30)
            if powerup_active and star_rect.collidepoint(mouse_x, mouse_y):
                freeze_until = current_time + 3.0 # Freeze for 3 seconds
                powerup_active = False # Hide it after use

            # 2. Check Alien Collision (Clicking Aliens)
            for a in aliens:
                alien_rect = pygame.Rect(a[0], a[1], 50, 50)
                if alien_rect.collidepoint(mouse_x, mouse_y):
                    a[1] = random.randint(-200, -50)
                    a[0] = random.randint(0, WIDTH - 50)

    # --- Logic & Movement ---
    # Only move aliens if we aren't frozen
    if current_time > freeze_until:
        for a in aliens:
            a[1] += a[2] # Move down
            if a[1] > HEIGHT: # Reset if they hit bottom
                a[1] = -50
                a[0] = random.randint(0, WIDTH - 50)
    
    # Randomly respawn powerup if it's gone
    if not powerup_active and current_time > freeze_until + 5:
        powerup_pos = [random.randint(50, WIDTH-50), random.randint(50, HEIGHT-50)]
        powerup_active = True

    # --- Drawing ---
    # Draw Powerup
    if powerup_active:
        screen.blit(star_surf, powerup_pos)
        # Optional: Add a glow effect if frozen
    
    # Draw Aliens
    for a in aliens:
        screen.blit(alien_surf, (a[0], a[1]))

    # UI Feedback
    if current_time < freeze_until:
        font = pygame.font.SysFont(None, 48)
        img = font.render("TIME FROZEN!", True, (0, 200, 255))
        screen.blit(img, (WIDTH//2 - 100, 20))

    pygame.display.flip()

pygame.quit()