import pyglet
import pymunk

from .entity import Entity
from globals import bullet_category, asteroid_category


class Bullet(Entity):
    def __init__(
        self,
        x: int,
        y: int,
        lives: int,
        angle: float = 0,
        batch: pyglet.graphics.Batch = None,
    ) -> None:
        image = pyglet.image.load(f"assets/laser{lives}.png")
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
        self.shape.filter = pymunk.ShapeFilter(
            categories=bullet_category, mask=asteroid_category
        )

        self.apply_impulse(pymunk.Vec2d(0, 900), self.body.angle)
