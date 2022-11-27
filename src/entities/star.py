import pyglet
import pymunk
from .entity import Entity
from globals import star_category, player_category


class Star(Entity):
    def __init__(
        self,
        x: int,
        y: int,
        batch: pyglet.graphics.Batch = None,
        width: int = 36,
    ):
        image = pyglet.image.load("assets/star.png")
        image.anchor_x = image.width // 2
        image.anchor_y = image.height // 2

        super().__init__(
            image,
            x,
            y,
            batch=batch,
            width=width,
        )

        self.shape.id = "star"
        self.shape.filter = pymunk.ShapeFilter(
            categories=star_category, mask=player_category
        )
