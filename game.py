import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Window setup
window_width, window_height = 800, 600
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Cell Game")

# Colors
# Function to generate a truly random color
def random_color():
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

clock = pygame.time.Clock()
fps = 60

def distance(x1, y1, x2, y2):
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

class Cell:
    def __init__(self, x, y, radius, color):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = random_color()
        self.speed = 4
        self.food_eaten = 0
        self.dx = random.randint(-1, 1)
        self.dy = random.randint(-1, 1)
        if self.dx == 0 and self.dy == 0:  # Prevent cells from being stationary
            self.dx = 1

    def draw(self, window):
        pygame.draw.circle(window, self.color, (self.x, self.y), self.radius)

    def move(self):
        self.x += self.dx * self.speed
        self.y += self.dy * self.speed
        # Prevent cells from moving outside window bounds
        if self.x - self.radius < 0 or self.x + self.radius > window_width:
            self.dx *= -1
        if self.y - self.radius < 0 or self.y + self.radius > window_height:
            self.dy *= -1

    def move_towards_food(self, foods):
        if foods:
            nearest_food = min(foods, key=lambda food: distance(self.x, self.y, food.x, food.y))
            dir_x, dir_y = nearest_food.x - self.x, nearest_food.y - self.y
            distance_to_food = distance(self.x, self.y, nearest_food.x, nearest_food.y)

            if distance_to_food != 0:
                dir_x, dir_y = dir_x / distance_to_food, dir_y / distance_to_food
                self.x += dir_x * self.speed
                self.y += dir_y * self.speed

    def eat_food(self, foods):
        action_required = None
        for food in foods[:]:
            if distance(self.x, self.y, food.x, food.y) < self.radius:
                foods.remove(food)
                self.food_eaten += 1
                self.radius += .25  # Cell grows in size
                self.speed *= .99  # Slightly reduce speed
                self.color = random_color()
                
                if self.food_eaten % 5  == 0:  # Spawn a new cell every 2 pieces of food
                    action_required = 'spawn_new_cell'
                
                if self.food_eaten == 100:  # Explode after eating 10 pieces of food
                    action_required = 'explode'
                    break
        return action_required

class Food:
    def __init__(self, x=None, y=None):
        self.x = random.randint(0, window_width) if x is None else x
        self.y = random.randint(0, window_height) if y is None else y
        self.radius = 2

    def draw(self, window):
        pygame.draw.circle(window, (0, 0, 0), (self.x, self.y), self.radius)

def check_cell_collision(cells):
    for i in range(len(cells)):
        for j in range(i + 1, len(cells)):
            cell1 = cells[i]
            cell2 = cells[j]
            dist = distance(cell1.x, cell1.y, cell2.x, cell2.y)
            if dist < cell1.radius + cell2.radius:
                # Simple bounce effect by swapping directions
                cell1.dx, cell2.dx = cell2.dx, cell1.dx
                cell1.dy, cell2.dy = cell2.dy, cell1.dy

                # Adjust positions to prevent overlapping
                overlap = cell1.radius + cell2.radius - dist
                if dist > 0:  # Prevent division by zero
                    dx = (cell1.x - cell2.x) / dist
                    dy = (cell1.y - cell2.y) / dist
                    cell1.x += dx * overlap / 2
                    cell2.x -= dx * overlap / 2
                    cell1.y += dy * overlap / 2
                    cell2.y -= dy * overlap / 2

def main():
    run = True
    cells = [Cell(random.randint(0, window_width), random.randint(0, window_height), 10, random_color()) for _ in range(1)]
    foods = []

    while run:
        window.fill((255, 255, 255))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        if random.randint(1, 200) > 195:  # Random food spawn
            foods.append(Food())

        check_cell_collision(cells)

        for cell in cells[:]:
            cell.move_towards_food(foods) if foods else cell.move()
            action = cell.eat_food(foods)
            if action == 'spawn_new_cell':
                # Spawn a new cell at a random position with a random color
                cells.append(Cell(random.randint(0, window_width), random.randint(0, window_height), 10, random_color()))
            elif action == 'explode':
                # Create new food where the cell exploded and remove the cell
                #for _ in range(10):
                    #foods.append(Food(cell.x, cell.y))
                cells.remove(cell)
            
            cell.draw(window)

        for food in foods:
            food.draw(window)

        pygame.display.update()
        clock.tick(fps)

    pygame.quit()

if __name__ == "__main__":
    main()
