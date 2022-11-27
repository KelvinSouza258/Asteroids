import pyglet

from globals import space
from src.core import Window, ScreenHandler
from src.screens import Home, Game, Retry

window = Window()

pyglet.font.add_file("assets/fonts/kenvector_future.ttf")
kenvector = pyglet.font.load("KenVector Future", 16)

counter = pyglet.window.FPSDisplay(window=window)
screen_handler = ScreenHandler()
home_screen = Home(window=window, screen_handler=screen_handler)

screen_handler.current = home_screen


@window.event
def on_draw():
    window.clear()
    screen_handler.draw()
    counter.draw()
    # space.debug_draw(options)


def update(dt):
    space.step(dt)
    screen_handler.update(dt)
    if isinstance(screen_handler.current, Game):
        if screen_handler.current.lives == 0:
            screen_handler.current = Retry(
                window=window,
                screen_handler=screen_handler,
                last_score=screen_handler.current.score,
            )


if __name__ == "__main__":
    pyglet.clock.schedule_interval(update, 1 / 120.0)

    pyglet.app.run()
