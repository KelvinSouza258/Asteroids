import pyglet


class Window(pyglet.window.Window):
    def __init__(self) -> None:
        super().__init__(
            caption="Asteroids",
            fullscreen=True,
        )
