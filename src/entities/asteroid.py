from math import radians
from random import randint
import pyglet
from .entity import Entity


import pymunk


class Asteroid(Entity):
    def __init__(self, x, y, batch=None, width=32):
        image = pyglet.image.load("assets/asteroids/meteorGrey_big1.png")
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

        force = pymunk.Vec2d(randint(5, 150), randint(5, 150))
        force.rotated(self.body.angle)
        self.body.apply_impulse_at_local_point(force)

        self.body.angular_velocity = radians(randint(-180, 180))
