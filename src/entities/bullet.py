import pyglet
import pymunk

from .entity import Entity
from globals import bullet_category


class Bullet(Entity):
    def __init__(self, x, y, angle=0, batch=None):
        image = pyglet.image.load("assets/laserBlue01.png")
        image.anchor_x = image.width // 2
        image.anchor_y = image.height // 2

        super().__init__(
            image,
            x,
            y,
            batch=batch,
            width=8,
        )

        self.shape.id = "bullet"
        self.body.angle = angle
        self.shape.filter = pymunk.ShapeFilter(bullet_category)

        force = pymunk.Vec2d(0, 900)
        force.rotated(self.body.angle)
        self.body.apply_impulse_at_local_point(force)
