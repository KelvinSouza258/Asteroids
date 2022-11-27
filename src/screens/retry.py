import pyglet
from .screen import Screen
from .game import Game
from src.core import Window, ScreenHandler


class Retry(Screen):
    def __init__(
        self, window: Window, screen_handler: ScreenHandler, last_score: int
    ) -> None:
        super().__init__()
        self.window = window
        self.window.push_handlers(self)
        self.screen_handler = screen_handler
        self.hud_batch = pyglet.graphics.Batch()
        self.title = pyglet.text.Label(
            text="Game Over",
            font_name="KenVector Future",
            x=window.width // 2,
            y=window.height // 2 + 50,
            anchor_x="center",
            anchor_y="center",
            font_size=40,
            batch=self.hud_batch,
        )
        self.last_score = pyglet.text.Label(
            text=f"Score: {last_score}",
            font_name="KenVector Future",
            x=window.width // 2,
            y=window.height // 2,
            anchor_x="center",
            anchor_y="center",
            font_size=20,
            batch=self.hud_batch,
        )
        self.label = pyglet.text.Label(
            text="Press SPACE to try again",
            font_name="KenVector Future",
            x=window.width // 2,
            y=window.height // 2 - 200,
            anchor_x="center",
            anchor_y="center",
            font_size=20,
            batch=self.hud_batch,
        )

    def draw(self) -> None:
        super().draw()
        self.hud_batch.draw()

    def on_key_press(self, symbol: int, modifiers: int) -> None:
        if self.screen_handler.current == self:
            if symbol == pyglet.window.key.SPACE:
                self.screen_handler.current = Game(
                    window=self.window,
                    screen_handler=self.screen_handler,
                )

    def update(self, dt: float) -> None:
        pass
