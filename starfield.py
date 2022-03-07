###############################################################################
# Playing with starfields in pygame
# Based upon CodingTrain StarField for Processing (P5) 
###############################################################################
import pygame

from sys import exit
from dataclasses import dataclass
from random import randint
from numpy import interp
from typing import Tuple


WIDTH = 800
HEIGHT = 600
TITLE = 'Starfield'
MAX_FRAME_RATE = 60


@dataclass
class Star:
    x: float
    y: float
    z: float

    def __init__(self):
        '''
        Randomise the position
        '''
        self.x = randint(-WIDTH, WIDTH)
        self.y = randint(-HEIGHT, HEIGHT)
        self.z = randint(1, WIDTH)
        self.pz = self.z

    def update(self) -> None:
        '''
        Z gets smaller as the star gets closer
        '''
        self.pz = self.z
        speed, _ = pygame.mouse.get_pos()
        self.z -= self.map(speed, 0, WIDTH, 0, 50)

        if self.z < 1:
            self.x = randint(-WIDTH, WIDTH)
            self.y = randint(-HEIGHT, HEIGHT)
            self.z = randint(1, WIDTH)

    def show(self, surface) -> None:
        '''
        Surface will be updated.
        '''
        sx, sy = self.remap()
        tx, ty = self.translate(sx, sy)
        r = self.radius()

        pygame.draw.ellipse(
            surface,
            'white',
            (tx, ty, r, r))

    def remap(self) -> Tuple[float, float]:
        '''
        Remaps to screen using z
        '''
        sx = self.map(self.x/self.z, 0, 1, 0, WIDTH)
        sy = self.map(self.y/self.z, 0, 1, 0, HEIGHT)
        return (sx, sy)

    def map(self, x, a, b, c, d):
        '''
        Re-map number x, with range a-b to new range c-c,
        this maintains ratio.
        '''
        w =  (x-a) / (b-a)
        y = c + w * (d-c)
        return y

    def translate(self, x , y) -> Tuple[float, float]:
        '''
        Translate the origin to the centre of the screen
        '''
        return x + (WIDTH / 2), y + (HEIGHT / 2)

    def radius(self):
        '''
        Radius dependent upon z, smaller z is closer
        '''
        return self.map(self.z, 1, WIDTH, 8, 0)


class StarField:
    '''
    Holds all the stars we have
    '''
    def __init__(self, num_stars=100):
        self.stars = [Star() for i in range(num_stars)]

    def draw(self, surface):
        '''
        Places the startfile on the surface
        '''
        surface.fill('black')
        for star in self.stars:
            star.update()
            star.show(surface)


starfeild = StarField(800)


def process_events() -> bool:
    '''
    Run through all events and perform actions on those that are important
    to us. Return True if we are still running, False otherwise.
    '''
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            return False
    return True


def event_loop():
    '''
    Main event loop
    '''
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(TITLE)
    clock = pygame.time.Clock()
    starfield_surface = pygame.Surface((WIDTH, HEIGHT))

    while process_events():
        starfeild.draw(starfield_surface)
        screen.blit(starfield_surface, (0, 0))
        pygame.display.update()
        clock.tick(MAX_FRAME_RATE)


if __name__ == '__main__':
    event_loop()
    exit()
