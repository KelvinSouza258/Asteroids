import pyglet
import pymunk

from math import degrees


class Entity(pyglet.sprite.Sprite):
    def __init__(self, image, x, y, width=32, batch=None):
        super().__init__(
            image,
            x=x,
            y=y,
            batch=batch,
        )

        self.scale = width / self.width
        self.moment = pymunk.moment_for_box(1, (self.width, self.height))
        self.body = pymunk.Body(1, self.moment)
        self.body.position = x, y
        self.shape = pymunk.Poly.create_box(
            self.body,
            (
                self.width,
                self.height,
            ),
        )
        self.shape.elasticity = 0
        self.shape.friction = 0

    def update(self, dt):
        self.rotation = -degrees(self.body.angle)
        self.position = self.body.position

    def __del__(self):
        super().delete()
