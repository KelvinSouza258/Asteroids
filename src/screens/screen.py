import pyglet


class Screen:
    def __init__(self) -> None:
        self.batch = pyglet.graphics.Batch()
        self.background_image = pyglet.image.load("assets/background.png")
        self.background_sprite = pyglet.sprite.Sprite(
            self.background_image,
        )

    def draw(self) -> None:
        self.background_sprite.draw()
        self.batch.draw()
