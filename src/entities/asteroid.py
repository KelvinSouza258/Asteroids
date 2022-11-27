from math import radians
from random import randint
import pyglet
from .entity import Entity


import pymunk


class Asteroid(Entity):
    def __init__(
        self,
        x: int,
        y: int,
        batch: pyglet.graphics.Batch = None,
        width: int = 32,
    ) -> None:
        image = pyglet.image.load(
            f"assets/asteroids/meteorGrey_big{randint(1,4)}.png",
        )
        image.anchor_x = image.width // 2
        image.anchor_y = image.height // 2

        super().__init__(
            image,
            x,
            y,
            batch=batch,
            width=width,
        )

        self.shape.id = "asteroid"

        if x < 640 and y < 360:
            self.body.angle = radians(randint(30, 60))
        elif x > 640 and y < 360:
            self.body.angle = radians(randint(120, 150))
        elif x < 640 and y > 360:
            self.body.angle = radians(randint(300, 330))
        elif x > 640 and y > 360:
            self.body.angle = radians(randint(210, 240))

        self.apply_impulse(
            pymunk.Vec2d(randint(5, 150), randint(5, 150)),
            self.body.angle,
        )

        self.body.angular_velocity = radians(randint(-180, 180))
