import pygame
import math

pygame.init()

WIDTH, HEIGHT = 1200, 900  
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Gravitational Slingshot Effect")

G = 6.67430e-11  # Gravitational constant
SCALE = 2e-7  # pixels per meter 

PLANET_MASS = 1.898e27  # mass of Jupiter in kg
SHIP_MASS = 1000        # kg
FPS = 60
PLANET_RADIUS = 7e7     # radius of Jupiter in meters
PLANET_SIZE = int(PLANET_RADIUS * SCALE * 2.5)  
OBJ_SIZE = 8

VEL_SCALE = 100  # pixels to velocity c

PLANET_IMG = pygame.transform.scale(pygame.image.load("jupiter.png"), (PLANET_SIZE * 2, PLANET_SIZE * 2))

WHITE = (255, 255, 255)
RED = (255, 0, 0)

font = pygame.font.SysFont("Arial", 16)

class Planet:
    def __init__(self, x, y, mass):
        self.x = x
        self.y = y
        self.mass = mass
    
    def draw(self):
        win.blit(PLANET_IMG, (self.x - PLANET_SIZE, self.y - PLANET_SIZE))

class Spacecraft:
    def __init__(self, x, y, vel_x, vel_y, mass):
        self.x = x
        self.y = y
        self.vel_x = vel_x
        self.vel_y = vel_y
        self.mass = mass

    def move(self, planet):
        dx = (planet.x - self.x)
        dy = (planet.y - self.y)
        distance_px = math.sqrt(dx ** 2 + dy ** 2)
        distance_m = distance_px / SCALE

        force = (G * self.mass * planet.mass) / distance_m ** 2
        acceleration = force / self.mass

        angle = math.atan2(dy, dx)
        acc_x = acceleration * math.cos(angle)
        acc_y = acceleration * math.sin(angle)

        self.vel_x += acc_x * SCALE
        self.vel_y += acc_y * SCALE

        self.x += self.vel_x
        self.y += self.vel_y

        return distance_m, force, self.speed()

    def speed(self):
        return math.sqrt(self.vel_x**2 + self.vel_y**2) / SCALE

    def draw(self):
        speed = self.speed()
        pygame.draw.circle(win, RED, (int(self.x), int(self.y)), OBJ_SIZE)
        v_text = font.render(f"velocity: {speed} m/s", True, WHITE)
        win.blit(v_text, (self.x, self.y+30))


def draw_variable_info(obj, dist_m, force, idx):
    speed = obj.speed()
    lines = [
        f"Spacecraft {idx + 1}",
        f"Speed: {speed:.2f} m/s",
        f"Distance: {dist_m/1000:.2f} km",
        f"Force: {force:.2e} N"
    ]
    for i, line in enumerate(lines):
        text = font.render(line, True, WHITE)
        win.blit(text, (10, 10 + idx * 70 + i * 18))

def create_ship(location, mouse):
    t_x, t_y = location
    m_x, m_y = mouse
    vel_x = (m_x - t_x) / VEL_SCALE
    vel_y = (m_y - t_y) / VEL_SCALE
    return Spacecraft(t_x, t_y, vel_x, vel_y, SHIP_MASS)

def main():
    running = True
    clock = pygame.time.Clock()

    planet = Planet(WIDTH // 2, HEIGHT // 2, PLANET_MASS)
    objects = []
    temp_obj_pos = None
    paused = False

    while running:
        clock.tick(FPS)
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_TAB:
                    paused = not paused

            if not paused and event.type == pygame.MOUSEBUTTONDOWN:
                if temp_obj_pos:
                    obj = create_ship(temp_obj_pos, mouse_pos)
                    objects.append(obj)
                    temp_obj_pos = None
                else:
                    temp_obj_pos = mouse_pos

        win.fill((0, 0, 0))

        if temp_obj_pos:
            pygame.draw.line(win, WHITE, temp_obj_pos, mouse_pos, 2)
            pygame.draw.circle(win, RED, temp_obj_pos, OBJ_SIZE)

        for idx, obj in enumerate(objects[:]):
            obj.draw()

            if not paused:
                dist_m, force, _ = obj.move(planet)
                draw_variable_info(obj, dist_m, force, idx)

                off_screen = obj.x < 0 or obj.x > WIDTH or obj.y < 0 or obj.y > HEIGHT
                collided = (dist_m <= PLANET_RADIUS)
                if off_screen or collided:
                    objects.remove(obj)
            else:
                dist_m = math.sqrt((obj.x - planet.x) ** 2 + (obj.y - planet.y) ** 2) / SCALE
                force = (G * obj.mass * planet.mass) / dist_m ** 2
                draw_variable_info(obj, dist_m, force, idx)

        planet.draw()

        if paused:
            pause_text = font.render("PAUSED (Press TAB to resume)", True, WHITE)
            win.blit(pause_text, (WIDTH - 260, HEIGHT - 30))

        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()
