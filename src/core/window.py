import pyglet


class Window(pyglet.window.Window):
    def __init__(self):
        super().__init__(
            caption="Asteroids",
            width=1280,
            height=720,
        )
