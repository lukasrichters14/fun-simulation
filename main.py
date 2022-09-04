import pygame
from pygame.locals import *
from random import randint, shuffle
from time import sleep


SCREEN_X = 750
SCREEN_Y = 550


class Particle(pygame.sprite.Sprite):
    def __init__(self, x, y, radius):
        super(Particle, self).__init__()
        self.surf = pygame.Surface((radius * 2, radius * 2))
        self.rect = self.surf.get_rect()
        self.x = x
        self.y = y

        rnd_color = randint(1, 100)
        if rnd_color <= 33:
            color = (0, 255, 255)
            self.speed_x = 2
            self.speed_y = 2
            self.change_direction_prob = 0.03
        elif 33 < rnd_color <= 66:
            color = (255, 0, 255)
            self.speed_x = 1
            self.speed_y = 1
            self.change_direction_prob = 0.06
        else:
            color = (255, 255, 0)
            self.speed_x = 1
            self.speed_y = 1
            self.change_direction_prob = 0.03

        self.color = color
        self.radius = radius
        self.colliding = False

    def draw(self):
        pygame.draw.circle(self.surf, self.color, (self.radius, self.radius), self.radius, 0)

    def update(self):
        change_x = randint(1, 100) / 100
        change_y = randint(1, 100) / 100
        if change_x < self.change_direction_prob:
            self.speed_x *= -1
        if change_y < self.change_direction_prob:
            self.speed_y *= -1

        self.x += self.speed_x
        self.y += self.speed_y
        if SCREEN_X - 10 <= self.x or self.x <= 50:
            self.speed_x *= -1
            self.x += self.speed_x * 2

        if SCREEN_Y - 10 <= self.y or self.y <= 50:
            self.speed_y *= -1
            self.y += self.speed_y * 2

        self.surf.fill((0, 0, 0), self.rect)
        self.draw()


def collide(a, b):
    a.color = b.color
    a.speed_y = b.speed_y * -1
    a.speed_x = b.speed_y * -1
    a.change_direction_prob = b.change_direction_prob


def check_collisions(particle_list):
    seen = set()
    for i in particle_list:
        i.colliding = False

    for i in particle_list:
        for j in particle_list:
            if i is not j and abs(i.x - j.x) <= i.radius * 2 and abs(i.y - j.y) <= i.radius * 2:
                if i not in seen and j not in seen and not i.colliding and not j.colliding:
                    i.colliding = True
                    j.colliding = True
                    seen.add(i)
                    seen.add(j)
                    change_color = randint(1, 100)
                    if change_color <= 50:
                        collide(i, j)
                    else:
                        collide(j, i)


if __name__ == "__main__":
    pygame.init()

    # Define the dimensions of screen object
    screen = pygame.display.set_mode((SCREEN_X + 50, SCREEN_Y + 50))

    particles = []
    for _ in range(30):
        particles.append(Particle(randint(51, SCREEN_X), randint(51, SCREEN_Y), 5))

    game = True
    while game:
        # for loop through the event queue
        for event in pygame.event.get():

            # Check for QUIT event
            if event.type == QUIT:
                game = False

        pygame.display.get_surface().fill((0, 0, 0))
        for particle in particles:
            particle.update()
            screen.blit(particle.surf, (particle.x, particle.y))

        check_collisions(particles)
        shuffle(particles)

        # Update the display using flip
        sleep(0.01)
        pygame.display.flip()
