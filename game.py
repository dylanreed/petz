import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants for the game
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
BACKGROUND_COLOR = (34, 139, 34)  # Forest Green
MENU_HEIGHT = 50
FOOD_COLOR = (128, 128, 128)  # Grey
FOOD_SIZE = 8  # Size of the food pixel
EXPLOSION_SIZE_THRESHOLD = 60  # Size threshold for explosion
MAX_PET_SPEED = 5  # Maximum speed of pets
CONSUME_TIME = 1  # Time in milliseconds to consume food

def generate_random_color():
    """Generate a random color."""
    return random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)

class Pet:
    def __init__(self, x, y, size=4):
        """Initialize a new pet."""
        self.x = x
        self.y = y
        self.size = size
        self.color = generate_random_color()  # Assign a unique random color
        self.speed = 3  # Initial speed
        self.direction = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])  # Random initial direction

    def update_movement(self, food_x, food_y):
        """Update the pet's movement towards food or randomly."""
        if food_x is not None and food_y is not None:
            # Move towards food
            dx = food_x - self.x
            dy = food_y - self.y
            dist = max(abs(dx), abs(dy))
            if dist > 0:
                self.x += self.speed * (dx / dist)
                self.y += self.speed * (dy / dist)
        else:
            # Random movement
            self.x += self.direction[0] * self.speed
            self.y += self.direction[1] * self.speed
            # Change direction randomly at times
            if random.randint(0, 20) == 0:
                self.direction = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])
            # Keep within screen bounds
            self.x = max(0, min(SCREEN_WIDTH - self.size, self.x))
            self.y = max(0, min(SCREEN_HEIGHT - self.size - MENU_HEIGHT, self.y))

    def grow_and_maybe_split(self):
        """Grow the pet and possibly split it."""
        self.size += 2
        self.speed = max(0.5, self.speed * 0.9)  # Decrease speed as size increases
        if self.size % 5 == 0:
            # Create and return a new pet if size is divisible by 5
            new_x = self.x + random.randint(-10, 10)
            new_y = self.y + random.randint(-10, 10)
            return Pet(new_x, new_y, size=self.size/2)
        return None

    def bounce_off(self, other_pet):
        """Bounce off another pet to avoid overlap."""
        dx = self.x - other_pet.x
        dy = self.y - other_pet.y
        if dx > 0: self.x += self.speed
        else: self.x -= self.speed
        if dy > 0: self.y += self.speed
        else: self.y -= self.speed

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Virtual Pet Game")

pets = [Pet(random.randint(100, SCREEN_WIDTH - 100), random.randint(100, SCREEN_HEIGHT - 100)) for _ in range(25)]
food_x, food_y = None, None
eating = False
last_eat_time = 0  # Track the last time a pet ate
game_running = True
inventory_selected = "food"

while game_running:
    current_time = pygame.time.get_ticks()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if mouse_y > SCREEN_HEIGHT - MENU_HEIGHT:
                inventory_selected = "food"
            elif inventory_selected == "food" and not eating and food_x is None and mouse_y < SCREEN_HEIGHT - MENU_HEIGHT:
                food_x, food_y = mouse_x, mouse_y
                last_eat_time = current_time  # Reset eating timer

    for pet in pets[:]:  # Iterate over a copy of the list
        pet.update_movement(food_x, food_y)
        if not eating and food_x is not None and abs(pet.x + pet.size // 2 - food_x) <= pet.size and abs(pet.y + pet.size // 2 - food_y) <= pet.size:
            new_pet = pet.grow_and_maybe_split()
            if new_pet:
                pets.append(new_pet)
            food_x, food_y = None, None
            eating = True
            last_eat_time = current_time

    if eating and current_time - last_eat_time > CONSUME_TIME:
        eating = False

    # Collision detection and response
    for i, pet1 in enumerate(pets):
        for pet2 in pets[i+1:]:
            if abs(pet1.x - pet2.x) < max(pet1.size, pet2.size) and abs(pet1.y - pet2.y) < max(pet1.size, pet2.size):
                pet1.bounce_off(pet2)
                pet2.bounce_off(pet1)

    screen.fill(BACKGROUND_COLOR)
    for pet in pets:
        pygame.draw.rect(screen, pet.color, (pet.x, pet.y, pet.size, pet.size))
    if food_x is not None and food_y is not None:
        pygame.draw.rect(screen, FOOD_COLOR, (food_x, food_y, FOOD_SIZE, FOOD_SIZE))
    pygame.draw.rect(screen, (200, 200, 200), (0, SCREEN_HEIGHT - MENU_HEIGHT, SCREEN_WIDTH, MENU_HEIGHT))

    pygame.display.flip()

    pygame.time.Clock().tick(60)

pygame.quit()
sys.exit()
