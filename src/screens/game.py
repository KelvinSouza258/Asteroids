import pyglet

from globals import space
from .screen import Screen
from src.core import load_asteroids, Window, ScreenHandler
from src.entities import Player, Asteroid, Bullet, Entity, Star
from random import randint


class Game(Screen):
    def __init__(self, window: Window, screen_handler: ScreenHandler) -> None:
        super().__init__()
        self.window = window
        self.screen_handler = screen_handler
        self.asteroids = load_asteroids(space=space, batch=self.batch)
        self.destroyed_shapes: list[Entity] = []
        self.hud_batch = pyglet.graphics.Batch()

        x, y = self.get_random_position()
        self.stars = [
            Star(
                x=x,
                y=y,
                batch=self.batch,
            )
        ]

        for star in self.stars:
            space.add(star.body, star.shape)

        # draw 3 lives
        self.lives = 3
        self.lives_sprites = [
            pyglet.sprite.Sprite(
                pyglet.image.load(f"assets/playerLife{i + 1}.png"),
                x=32 + (56 * i),
                y=window.height - 48,
                batch=self.hud_batch,
            )
            for i in range(self.lives)
        ]

        self.player = Player(
            width=64,
            lives=self.lives,
            window=window,
            batch=self.batch,
        )

        self.score = 0
        self.label_score = pyglet.text.Label(
            text=f"Score: {self.score}",
            font_name="KenVector Future",
            x=window.width - 20,
            y=window.height - 10,
            anchor_x="right",
            anchor_y="top",
            font_size=20,
            batch=self.hud_batch,
        )

        space.add(self.player.body, self.player.shape)

        window.push_handlers(self.player)

        def collision_begin(arbiter, space, data):
            first_shape, second_shape = arbiter.shapes

            if (
                first_shape == self.player.shape
                and second_shape.id == "asteroid"  # noqa: E501
            ):
                self.destroyed_shapes.append(second_shape)
                self.lose_live()
            elif (
                first_shape.id == "asteroid"
                and second_shape == self.player.shape  # noqa: E501
            ):
                self.destroyed_shapes.append(first_shape)
                self.lose_live()
            # star collision + 10 points
            elif (
                first_shape == self.player.shape
                and second_shape.id == "star"  # noqa: E501
            ):
                self.score += 15
                self.destroyed_shapes.append(second_shape)
            elif (
                first_shape.id == "star"
                and second_shape == self.player.shape  # noqa: E501
            ):
                self.score += 15
                self.destroyed_shapes.append(first_shape)

            elif first_shape.id == "bullet" and second_shape.id == "asteroid":
                self.destroyed_shapes.extend([first_shape, second_shape])
                self.score += 1

            elif first_shape.id == "asteroid" and second_shape.id == "bullet":
                self.destroyed_shapes.extend([first_shape, second_shape])
                self.score += 1

            return True

        handler = space.add_default_collision_handler()
        handler.begin = collision_begin

    def get_random_position(self):
        return (
            randint(100, self.window.width - 100),
            randint(100, self.window.height - 100),
        )

    def add_star(self):
        x, y = self.get_random_position()
        star = Star(
            x=x,
            y=y,
            batch=self.batch,
        )
        self.stars.append(star)
        space.add(star.body, star.shape)

    def lose_live(self):
        self.lives -= 1
        if self.lives >= 0:
            self.lives_sprites[self.lives].delete()
            self.lives_sprites.pop(self.lives)

        self.player.reset(self.lives)

    def draw(self) -> None:
        super().draw()
        self.hud_batch.draw()

    def update(self, dt):
        self.label_score.text = f"Score: {self.score}"
        game_objects = (
            [self.player] + self.stars + self.player.shots + self.asteroids
        )  # noqa: E501

        for obj in game_objects:
            obj.update(dt)

            if isinstance(obj, Asteroid):
                if (
                    obj.x < -400
                    or obj.x > self.window.width + 400
                    or obj.y < -400
                    or obj.y > self.window.height + 400
                    or obj.shape in self.destroyed_shapes
                ):
                    self.asteroids.remove(obj)
                    space.remove(obj.body, obj.shape)
                    del obj
            elif isinstance(obj, Bullet):
                if (
                    obj.x < 0
                    or obj.x > self.window.width
                    or obj.y < 0
                    or obj.y > self.window.height
                    or obj.shape in self.destroyed_shapes
                ):
                    self.player.shots.remove(obj)
                    space.remove(obj.body, obj.shape)
                    del obj

            elif isinstance(obj, Star):
                if obj.shape in self.destroyed_shapes:
                    self.stars.remove(obj)
                    space.remove(obj.body, obj.shape)
                    del obj

            if len(self.asteroids) < 15:
                self.asteroids.extend(
                    load_asteroids(
                        space=space,
                        batch=self.batch,
                    )
                )

    def __del__(self):
        try:
            for obj in (
                [self.player]
                + self.stars
                + self.player.shots
                + self.asteroids  # noqa: E501
            ):
                space.remove(obj.body, obj.shape)
                del obj
        except AttributeError:
            pass
