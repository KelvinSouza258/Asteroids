import random

from src.entities import Asteroid
from pymunk import Space
from pyglet import graphics


def load_asteroids(space: Space, batch: graphics.Batch) -> list[Asteroid]:
    asteroids: list[Asteroid] = []
    for i in range(20):
        x = random.choice(
            [random.randint(-200, 0), random.randint(1280, 1480)],
        )
        y = random.choice(
            [random.randint(-200, 0), random.randint(720, 920)],
        )
        asteroid = Asteroid(
            x=x,
            y=y,
            batch=batch,
            width=random.randint(64, 128),
        )
        asteroids.append(asteroid)
        space.add(asteroid.body, asteroid.shape)

    return asteroids
