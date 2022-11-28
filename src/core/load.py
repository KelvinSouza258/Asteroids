import random

from src.entities import Asteroid
from src.core import Window
from pymunk import Space
from pyglet import graphics


def load_asteroids(space: Space, batch: graphics.Batch, window: Window) -> list[Asteroid]:
    asteroids: list[Asteroid] = []
    for i in range(20):
        x = random.choice(
            [random.randint(-200, 0), random.randint(window.width, window.width + 200)],
        )
        y = random.choice(
            [random.randint(-200, 0), random.randint(window.height, window.height + 200)],
        )
        asteroid = Asteroid(
            x=x,
            y=y,
            window=window,
            batch=batch,
            width=random.randint(64, 128),
        )
        asteroids.append(asteroid)
        space.add(asteroid.body, asteroid.shape)

    return asteroids
