import pyglet
import pymunk

from math import degrees


class Entity(pyglet.sprite.Sprite):
    def __init__(
        self,
        image: pyglet.image.AbstractImage,
        x: int,
        y: int,
        width: int = 32,
        batch: pyglet.graphics.Batch = None,
    ) -> None:
        super().__init__(
            image,
            x=x,
            y=y,
            batch=batch,
        )

        self.scale = width / self.width
        self._moment = pymunk.moment_for_box(1, (self.width, self.height))
        self._body = pymunk.Body(1, self._moment)
        self._body.position = x, y
        self._shape = pymunk.Poly.create_box(
            self._body,
            (
                self.width,
                self.height,
            ),
        )
        self._shape.elasticity = 0
        self._shape.friction = 0

    @property
    def body(self) -> pymunk.Body:
        return self._body

    @property
    def shape(self) -> pymunk.Poly:
        return self._shape

    def update(self, dt) -> None:
        self.rotation = -degrees(self._body.angle)
        self.position = self._body.position

    def apply_impulse(self, force: pymunk.Vec2d, angle: float = 0) -> None:
        force.rotated(angle)
        self.body.apply_impulse_at_local_point(force)

    def __del__(self):
        super().delete()
